# Translation Endpoint for Globalhack 7

This is just a simple REST endpoint for teams to use for quickly translating text.  All it takes is a POST request to the endpoint below with a simple JSON payload to return a translated version of your text.

Powered by AWS Lambda and Google's Translate API

## Example

Example payload:
{
    "text": "How to get a job",
    "target_language": "es"
}

Sample call:
`curl {temporary_endpoint_from_slack} -d '{"text": "How to get a job", "target_language": "es"}'`

> Cómo conseguir trabajo