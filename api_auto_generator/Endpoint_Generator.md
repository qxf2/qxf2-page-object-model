# Auto Generate Endpoint modules for API Automation Framework #
The Endpoint generator project helps automate creating API automation tests using <a href="https://qxf2.com">Qxf2's</a> <a href="https://qxf2.com/blog/easily-maintainable-api-test-automation-framework/">API Automation framework</a>. It generates Endpoint modules - an abstraction for endpoints in the application under test from an <a href="https://learn.openapis.org/introduction.html">OpenAPI specification</a>.

## Requirements ##
- An V3.x.x OpenAPI specification for your API app.
- The spec file can be a `JSON` or `YAML` file.

## How to run the script? ##
- Validate the OpenAPI specification
```
python api_auto_generator/endpoint_module_generator --spec <OpenAPI_spec_file_location>
```
This command will help check if the OpenAPI spec can be used to generate Endpoints file. It will raise an exception for invalid or incomplete specs.
- Generate the `Endpoint` module
```
python api_auto_generator/endpoint_module_generator --spec <OpenAPI_spec_file_location> --generate-endpoints
```
This command will generate `<endpoint_name>_Endpoint.py` module in the `endpoints` dir.

## How does the script work? ##
- The script uses `openapi3_parser` module to parse and read the contents from an OpenAPI spec.
- The endpoints and its details are read from the spec
- A module-name, class-name, instance-method-names are all generated for the endpoint
- The Path & Query parameters to be passed to the Endpoint class is generated
- The json/data params to be passed to the requests method is generated from the request body
- A Python dictionary collecting all these values is generated
- Tge generated Python dictionary is redered on a Jinja2 template

## Limitations/Constraints on using the Generate Endpoint script ##

### Invalid OpenAPI spec ###
- The Generate Endpoint script validates the OpenAPI spec at the start of the execution, using an invalid spec triggers an exception
- The JSON Schema validation is also done in step #1, but the exception raised regarding a JSON Schema error can sometimes be a little confusing, in such cases replace the failing schema with {} to proceed to generate Endpoint files

### Minimal spec ###
- When using a minimal spec, to check if Endpoint files can be generated from it, run the script using --spec CLI param alone, you can proceed to use --generate-endpoint param if no issue was seen with the previous step