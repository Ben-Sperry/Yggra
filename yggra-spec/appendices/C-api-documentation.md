# Appendix C: API Documentation

## Core APIs

The Yggra system exposes several core APIs that enable applications to interact with personal data while maintaining privacy and consistency guarantees. Each API is designed to be intuitive while enforcing the system's fundamental principles.

### Graph API

The Graph API provides direct access to the graph layer, though most applications should interact through facets instead. This API is primarily used by system components and advanced applications that need fine-grained control.

```python
class GraphAPI:
    def create_entity() -> UUID:
        """
        Creates a new entity in the graph.
        
        Returns:
            UUID: The unique identifier for the new entity
            
        Raises:
            AuthorizationError: If the caller lacks permission to create entities
            GraphError: If the operation fails
        
        Example:
            entity_id = graph.create_entity()
        """
        
    def add_statement(subject: UUID, predicate: UUID, object: Any) -> UUID:
        """
        Adds a new statement to the graph. Statements are immutable once created.
        
        Args:
            subject: The entity this statement is about
            predicate: The property being defined
            object: The value or reference to another entity
            
        Returns:
            UUID: The unique identifier for the new statement
            
        Raises:
            ValidationError: If the statement structure is invalid
            AuthorizationError: If the caller lacks permission
            GraphError: If the operation fails
            
        Example:
            stmt_id = graph.add_statement(
                subject=photo_id,
                predicate=properties.TAKEN_ON,
                object=datetime.now()
            )
        """
        
    def query_statements(
        pattern: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Iterator[Statement]:
        """
        Queries statements matching the given pattern.
        
        Args:
            pattern: Dictionary specifying subject/predicate/object constraints
            limit: Maximum number of statements to return
            offset: Number of matching statements to skip
            
        Returns:
            Iterator yielding matching statements
            
        Example:
            # Find all photos taken in the last week
            recent_photos = graph.query_statements({
                'predicate': properties.TAKEN_ON,
                'object': lambda date: date > week_ago
            })
        """
```

### Facet API

The Facet API is the primary interface for applications. It enables them to interact with graph data through familiar data structures while maintaining consistency and privacy guarantees.

```python
class FacetAPI:
    def register_facet(
        name: str,
        schema: Dict[str, Any],
        handlers: Dict[str, Callable]
    ) -> UUID:
        """
        Registers a new facet definition with the system.
        
        Args:
            name: Unique identifier for this facet
            schema: Definition of the facet's data structure
            handlers: Functions for converting between facet and graph formats
            
        Returns:
            UUID: Identifier for the registered facet
            
        Example:
            contact_facet = facets.register_facet(
                name="contacts",
                schema={
                    "fields": {
                        "name": {"type": "text", "required": True},
                        "email": {"type": "email"},
                        "phone": {"type": "phone_number"}
                    },
                    "indexes": ["name", "email"]
                },
                handlers={
                    "to_graph": contact_to_graph,
                    "from_graph": graph_to_contact
                }
            )
        """
        
    def create_facet_instance(
        facet_id: UUID,
        config: Dict[str, Any]
    ) -> FacetInstance:
        """
        Creates a new instance of a registered facet.
        
        Args:
            facet_id: Identifier of the registered facet
            config: Configuration for this instance
            
        Returns:
            FacetInstance: The initialized facet instance
            
        Example:
            personal_contacts = facets.create_facet_instance(
                facet_id=contact_facet,
                config={
                    "storage": "sqlite",
                    "cache_policy": "write_through",
                    "privacy": {
                        "sharing": "explicit_only",
                        "encryption": "required"
                    }
                }
            )
        """
```

### Storage API

The Storage API enables integration of different storage backends while maintaining consistent behavior and security guarantees.

```python
class StorageAPI:
    def store(
        data: bytes,
        metadata: Dict[str, Any]
    ) -> StorageReference:
        """
        Stores data using the appropriate storage backend.
        
        Args:
            data: The binary data to store
            metadata: Information about the data and storage requirements
            
        Returns:
            StorageReference: Reference for retrieving the stored data
            
        Example:
            photo_ref = storage.store(
                data=photo_bytes,
                metadata={
                    "type": "image/jpeg",
                    "sensitivity": "private",
                    "access_pattern": "frequent_read"
                }
            )
        """
        
    def retrieve(
        reference: StorageReference,
        range: Optional[Range] = None
    ) -> bytes:
        """
        Retrieves stored data using its reference.
        
        Args:
            reference: The storage reference returned from store()
            range: Optional byte range for partial retrieval
            
        Returns:
            bytes: The requested data
            
        Example:
            # Retrieve just the first megabyte
            preview = storage.retrieve(
                reference=photo_ref,
                range=Range(0, 1_000_000)
            )
        """
```

### Sharing API

The Sharing API enables controlled data sharing between users while maintaining privacy and security.

```python
class SharingAPI:
    def create_shared_facet(
        source_facet: UUID,
        recipient: str,
        permissions: Dict[str, Any],
        expiration: Optional[datetime] = None
    ) -> ShareToken:
        """
        Creates a shared facet for another user to access.
        
        Args:
            source_facet: The facet to share
            recipient: Identifier of the recipient
            permissions: Access control specifications
            expiration: When the share should expire
            
        Returns:
            ShareToken: Token for accessing the shared facet
            
        Example:
            token = sharing.create_shared_facet(
                source_facet=photo_album,
                recipient="alice@example.com",
                permissions={
                    "operations": ["read"],
                    "fields": ["image", "date"],
                    "transformations": ["watermark"]
                },
                expiration=tomorrow
            )
        """
```

## Best Practices

When using these APIs, developers should follow these guidelines:

1. Always interact through facets unless you have a specific need for direct graph access.

2. Design facets to be minimal, requesting only the data structures your application actually needs.

3. Use the storage API's metadata to help the system optimize data placement.

4. Always specify explicit expiration times for shared facets.

5. Handle all errors gracefully, especially temporary failures in distributed operations.

## Error Handling

All APIs use a consistent error hierarchy:

```python
class YggraError(Exception):
    """Base class for all Yggra errors"""
    
class AuthorizationError(YggraError):
    """The operation is not permitted"""
    
class ValidationError(YggraError):
    """The input is invalid"""
    
class ConsistencyError(YggraError):
    """A consistency check failed"""
    
class StorageError(YggraError):
    """A storage operation failed"""
```

Applications should catch and handle these errors appropriately. Temporary failures can often be resolved by retrying the operation, while authorization or validation errors typically require application or user intervention.

## Rate Limiting and Quotas

The APIs implement rate limiting and quota management to ensure system stability:

- API calls are limited to 1000 per minute per application
- Storage operations are limited by available space
- Query complexity is limited to prevent resource exhaustion
- Shared facets have configurable access frequency limits

Applications should monitor these limits and handle limitation errors gracefully.