from drf_spectacular.generators import SchemaGenerator

class CustomSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # add your custom schema information here
        schema['info']['title'] = 'RecipeApp API'
        schema['info']['version'] = '1.0.0'
        schema['info']['description'] = 'Your custom API description'
        return schema
