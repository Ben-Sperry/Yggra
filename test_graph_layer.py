import unittest
from datetime import datetime
from graph_layer_core import GraphLayer, EntityType, EntityId, Entity, Statement

class TestGraphLayer(unittest.TestCase):
    def setUp(self):
        """Creates a fresh graph instance before each test."""
        self.graph = GraphLayer(node_id="test_node")

    def test_entity_creation(self):
        """Tests that we can create entities and they have correct properties."""
        # Create a standard entity
        entity = self.graph.create_entity()
        
        # Verify entity structure
        self.assertIsInstance(entity, Entity)
        self.assertIsInstance(entity.id, EntityId)
        self.assertEqual(entity.id.id_type, EntityType.STANDARD)
        self.assertEqual(entity.id.node_id, "test_node")
        
        # Verify entity is stored in graph
        self.assertIn(entity.id, self.graph.entities)

    def test_property_creation(self):
        """Tests creation of property entities."""
        # Create a property entity
        property_entity = self.graph.create_entity(EntityType.PROPERTY)
        
        # Verify property structure
        self.assertEqual(property_entity.id.id_type, EntityType.PROPERTY)
        self.assertIn(property_entity.id, self.graph.entities)

    def test_label_management(self):
        """Tests adding and retrieving labels."""
        entity = self.graph.create_entity()
        
        # Add a label
        self.graph.add_label(entity.id, "Test Entity")
        
        # Verify label retrieval
        label = self.graph.get_latest_label(entity.id)
        self.assertEqual(label, "Test Entity")
        
        # Test multiple labels in different languages
        self.graph.add_label(entity.id, "Test Entity FR", "fr")
        self.graph.add_label(entity.id, "Test Entity DE", "de")
        
        self.assertEqual(self.graph.get_latest_label(entity.id, "fr"), "Test Entity FR")
        self.assertEqual(self.graph.get_latest_label(entity.id, "de"), "Test Entity DE")

    def test_statement_creation(self):
        """Tests creating and storing statements."""
        # Create entities for our test
        person = self.graph.create_entity()
        name_prop = self.graph.create_entity(EntityType.PROPERTY)
        
        # Create a statement
        statement = self.graph.add_statement(
            subject=person.id,
            predicate=name_prop.id,
            object_="John Doe"
        )
        
        # Verify statement structure
        self.assertIsInstance(statement, Statement)
        self.assertEqual(statement.subject, person.id)
        self.assertEqual(statement.predicate, name_prop.id)
        self.assertEqual(statement.object, "John Doe")
        self.assertEqual(statement.node_id, "test_node")
        
        # Verify statement is stored in graph
        self.assertIn(statement, self.graph.statements)

    def test_merge_operation(self):
        """Tests merging two graphs."""
        # Create a second graph
        other_graph = GraphLayer(node_id="other_node")
        
        # Add some data to both graphs
        entity1 = self.graph.create_entity()
        self.graph.add_label(entity1.id, "Entity 1")
        
        entity2 = other_graph.create_entity()
        other_graph.add_label(entity2.id, "Entity 2")
        
        # Merge graphs
        self.graph.merge(other_graph)
        
        # Verify merged state
        self.assertTrue(all(
            entity_id in self.graph.entities
            for entity_id in other_graph.entities
        ))
        
        # Verify we can get labels from both original graphs
        self.assertEqual(self.graph.get_latest_label(entity1.id), "Entity 1")
        self.assertEqual(self.graph.get_latest_label(entity2.id), "Entity 2")

    def test_real_world_scenario(self):
        """Tests a realistic usage scenario."""
        # Create property types we'll need
        name_prop = self.graph.create_entity(EntityType.PROPERTY)
        self.graph.add_label(name_prop.id, "full name")
        
        email_prop = self.graph.create_entity(EntityType.PROPERTY)
        self.graph.add_label(email_prop.id, "email address")
        
        # Create a person entity
        person = self.graph.create_entity()
        self.graph.add_label(person.id, "John Smith")
        
        # Add statements about the person
        self.graph.add_statement(person.id, name_prop.id, "John Smith")
        self.graph.add_statement(person.id, email_prop.id, "john@example.com")
        
        # Verify everything is stored correctly
        self.assertEqual(self.graph.get_latest_label(person.id), "John Smith")
        self.assertGreaterEqual(len(self.graph.statements), 2)

if __name__ == '__main__':
    unittest.main()