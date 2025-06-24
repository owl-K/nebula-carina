"""
Backward Compatibility Tests for Pydantic 2.x Upgrade

This test file ensures that all existing methods from Pydantic 1.x
continue to work in Pydantic 2.x without any breaking changes.
"""

import unittest
from datetime import datetime, date, time
from typing import Optional

from nebula_carina.models import models
from nebula_carina.models.fields import create_nebula_field as _
from nebula_carina.ngql.schema import data_types


class TestTagModel(models.TagModel):
    """Test tag model for compatibility testing"""
    name: str = _(data_types.FixedString(30), ..., )
    age: int = _(data_types.Int16, ..., )
    created_on: datetime = _(data_types.Datetime, data_types.Datetime.auto)
    is_active: bool = _(data_types.Bool, True)


class TestEdgeTypeModel(models.EdgeTypeModel):
    """Test edge type model for compatibility testing"""
    weight: float = _(data_types.Float, ..., )
    description: str = _(data_types.String, "", )


class TestVertexModel(models.VertexModel):
    """Test vertex model for compatibility testing"""
    tag: TestTagModel


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility of all methods"""

    def setUp(self):
        """Set up test data"""
        self.test_tag = TestTagModel(
            name="test_name",
            age=25,
            created_on=datetime(2023, 1, 1, 12, 0, 0),
            is_active=True
        )
        
        self.test_edge_type = TestEdgeTypeModel(
            weight=1.5,
            description="test edge"
        )
        
        self.test_vertex = TestVertexModel(
            vid="test_vid_123",
            tag=self.test_tag
        )

    def test_tag_model_methods(self):
        """Test all TagModel methods exist and work"""
        # Test basic methods
        self.assertTrue(hasattr(TestTagModel, 'db_name'))
        self.assertTrue(hasattr(TestTagModel, 'get_db_name_pattern'))
        self.assertTrue(hasattr(TestTagModel, 'from_tag'))
        self.assertTrue(hasattr(TestTagModel, 'get_db_field_names'))
        self.assertTrue(hasattr(TestTagModel, 'get_db_field_dict'))
        self.assertTrue(hasattr(TestTagModel, 'get_db_field_value'))
        
        # Test instance methods
        self.assertTrue(hasattr(self.test_tag, 'get_db_field_dict'))
        self.assertTrue(hasattr(self.test_tag, 'get_db_field_value'))
        
        # Test method calls
        db_name = TestTagModel.db_name()
        self.assertEqual(db_name, 'test_tag_model')
        
        field_names = TestTagModel.get_db_field_names()
        expected_fields = ['name', 'age', 'created_on', 'is_active']
        self.assertEqual(set(field_names), set(expected_fields))
        
        field_dict = self.test_tag.get_db_field_dict()
        self.assertIn('name', field_dict)
        self.assertIn('age', field_dict)

    def test_edge_type_model_methods(self):
        """Test all EdgeTypeModel methods exist and work"""
        # Test basic methods
        self.assertTrue(hasattr(TestEdgeTypeModel, 'db_name'))
        self.assertTrue(hasattr(TestEdgeTypeModel, 'get_db_name_pattern'))
        self.assertTrue(hasattr(TestEdgeTypeModel, 'from_props'))
        self.assertTrue(hasattr(TestEdgeTypeModel, 'get_db_field_names'))
        self.assertTrue(hasattr(TestEdgeTypeModel, 'get_db_field_dict'))
        self.assertTrue(hasattr(TestEdgeTypeModel, 'get_db_field_value'))
        
        # Test method calls
        db_name = TestEdgeTypeModel.db_name()
        self.assertEqual(db_name, 'test_edge_type_model')
        
        field_names = TestEdgeTypeModel.get_db_field_names()
        expected_fields = ['weight', 'description']
        self.assertEqual(set(field_names), set(expected_fields))

    def test_vertex_model_methods(self):
        """Test all VertexModel methods exist and work"""
        # Test basic methods
        self.assertTrue(hasattr(TestVertexModel, 'get_db_name_pattern'))
        self.assertTrue(hasattr(TestVertexModel, 'iterate_tag_models'))
        self.assertTrue(hasattr(TestVertexModel, 'get_tag_name2model'))
        self.assertTrue(hasattr(TestVertexModel, 'from_vertex'))
        self.assertTrue(hasattr(TestVertexModel, 'from_nebula_db_cls'))
        
        # Test instance methods - CRITICAL FOR BACKWARD COMPATIBILITY
        self.assertTrue(hasattr(self.test_vertex, 'save'), "save() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'insert'), "insert() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'upsert'), "upsert() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'get_out_edges'), "get_out_edges() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'get_destinations'), "get_destinations() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'get_reverse_edges'), "get_reverse_edges() method must exist")
        self.assertTrue(hasattr(self.test_vertex, 'get_sources'), "get_sources() method must exist")
        
        # Test method calls
        tag_models = list(TestVertexModel.iterate_tag_models())
        self.assertEqual(len(tag_models), 1)
        self.assertEqual(tag_models[0][0], 'tag')
        self.assertEqual(tag_models[0][1], TestTagModel)

    def test_edge_model_methods(self):
        """Test all EdgeModel methods exist and work"""
        test_edge = models.EdgeModel(
            src_vid="src_123",
            dst_vid="dst_456",
            ranking=0,
            edge_type=self.test_edge_type
        )
        
        # Test basic methods
        self.assertTrue(hasattr(models.EdgeModel, 'get_db_name_pattern'))
        self.assertTrue(hasattr(models.EdgeModel, 'from_edge'))
        self.assertTrue(hasattr(models.EdgeModel, 'from_nebula_db_cls'))
        
        # Test instance methods - CRITICAL FOR BACKWARD COMPATIBILITY
        self.assertTrue(hasattr(test_edge, 'save'), "save() method must exist")
        self.assertTrue(hasattr(test_edge, 'insert'), "insert() method must exist")
        self.assertTrue(hasattr(test_edge, 'upsert'), "upsert() method must exist")
        self.assertTrue(hasattr(test_edge, 'get_edge_type_and_model'), "get_edge_type_and_model() method must exist")
        
        # Test method calls
        edge_type_name, edge_type_class = test_edge.get_edge_type_and_model()
        self.assertEqual(edge_type_name, 'test_edge_type_model')
        self.assertEqual(edge_type_class, TestEdgeTypeModel)

    def test_field_creation_compatibility(self):
        """Test field creation methods are compatible"""
        # Test create_nebula_field function
        field = _(
            data_types.String,
            default="test",
            description="test field",
            alias="test_alias"
        )
        
        self.assertTrue(hasattr(field, 'data_type'))
        self.assertTrue(hasattr(field, 'default'))
        self.assertTrue(hasattr(field, 'description'))
        self.assertTrue(hasattr(field, 'alias'))
        self.assertTrue(hasattr(field, 'create_db_field'))

    def test_data_types_compatibility(self):
        """Test all data types work correctly"""
        # Test String
        string_field = _(data_types.String, "test")
        self.assertEqual(string_field.data_type.value2db_str("hello"), '"hello"')
        
        # Test Int16
        int_field = _(data_types.Int16, 42)
        self.assertEqual(int_field.data_type.value2db_str(42), '42')
        
        # Test Bool
        bool_field = _(data_types.Bool, True)
        self.assertEqual(bool_field.data_type.value2db_str(True), 'true')
        
        # Test Date
        date_field = _(data_types.Date, date(2023, 1, 1))
        self.assertEqual(date_field.data_type.value2db_str(date(2023, 1, 1)), 'date("2023-01-01")')
        
        # Test Datetime
        dt_field = _(data_types.Datetime, datetime(2023, 1, 1, 12, 0, 0))
        self.assertIsNotNone(dt_field.data_type.value2db_str(datetime(2023, 1, 1, 12, 0, 0)))

    def test_model_fields_access(self):
        """Test model_fields access is compatible"""
        # Test TagModel fields
        tag_fields = TestTagModel.model_fields
        self.assertIn('name', tag_fields)
        self.assertIn('age', tag_fields)
        self.assertIn('created_on', tag_fields)
        self.assertIn('is_active', tag_fields)
        
        # Test VertexModel fields
        vertex_fields = TestVertexModel.model_fields
        self.assertIn('vid', vertex_fields)
        self.assertIn('tag', vertex_fields)

    def test_import_compatibility(self):
        """Test all imports work correctly"""
        # Test main imports
        from nebula_carina.models import models
        from nebula_carina.models.fields import create_nebula_field
        from nebula_carina.ngql.schema import data_types
        
        # Test specific class imports
        from nebula_carina.models.models import (
            BaseModel, TagModel, EdgeTypeModel, VertexModel, EdgeModel
        )
        
        # Verify classes exist
        self.assertTrue(issubclass(TagModel, BaseModel))
        self.assertTrue(issubclass(EdgeTypeModel, BaseModel))
        self.assertTrue(issubclass(VertexModel, BaseModel))
        self.assertTrue(issubclass(EdgeModel, BaseModel))

    def test_method_signatures(self):
        """Test method signatures are compatible"""
        # Test save method signature
        save_method = getattr(self.test_vertex, 'save')
        import inspect
        sig = inspect.signature(save_method)
        self.assertIn('if_not_exists', sig.parameters)
        
        # Test insert method signature
        insert_method = getattr(self.test_vertex, 'insert')
        sig = inspect.signature(insert_method)
        self.assertIn('if_not_exists', sig.parameters)

    def test_objects_manager(self):
        """Test objects manager exists and works"""
        # Test VertexModel objects
        self.assertTrue(hasattr(TestVertexModel, 'objects'))
        
        # Test EdgeModel objects
        self.assertTrue(hasattr(models.EdgeModel, 'objects'))


if __name__ == '__main__':
    unittest.main() 