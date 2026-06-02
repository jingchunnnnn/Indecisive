# Google Places Usage

Indecisive uses Places API New Text Search from the backend only.

## Search

The backend sends one Text Search request per recommendation request. It uses `locationBias`, then computes distance and ranking itself.

Field mask:

```text
places.id,places.name,places.displayName,places.formattedAddress,places.location,places.types,places.primaryType,places.googleMapsUri
```

Mappings:

- Google `id` -> `place_id`
- Google `name` -> optional `resource_name`
- Google `displayName.text` -> `name`

## Place Details

The detail page calls backend `GET /places/{place_id}`, which calls:

```text
GET https://places.googleapis.com/v1/places/{place_id}
```

Field mask:

```text
id,displayName,formattedAddress,location,types,primaryType,googleMapsUri
```

## Cost Control

- Keep the API key backend-only.
- Use strict field masks.
- Avoid photos, reviews, ratings, opening hours, price level, website URI, and generative summaries in the MVP.
- Use Place Details only when opening a detail page.
- Return a friendly service-unavailable error without an API key.
- Set Google Cloud budget alerts.
- Set daily quotas where possible.
- Validate radius and remarks to reduce accidental abuse.
- Use an 8-second backend timeout for Google requests.
