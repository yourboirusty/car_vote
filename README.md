# Ulam recrutation REST API
## Assumptions
1. User sign-in endpoint also provides a verification endpoint using the token,
2. Adding products should not be handled via API but still should be contained within the same application.
## Prerequisites
Docker-compose
## Run command
`cp .env.template .env`

`docker-compose up`
## API
[Full documentation here](https://documenter.getpostman.com/view/9607222/SztHW4xi)
### Authorization
Bearer token in headers

`Authorization: Bearer <token>`
### Listing products
`/products/`

Allowed methods: `GET`

Default pagination set to 25. Supports `offset=n` and `limit=n`.
#### Example output

```
{
    "count": 35,
    "next": "http://localhost:8080/products/?limit=25&offset=25",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "TestProduct0",
            "price": "0"
        },
		...
}
```

### Order management
Requires authorization headers

List view: `/orders/`
Allowed methods: `GET`, `POST`

Detailed view: `/orders/<pk>/`
Allowed methods: `PUT`, `PATCH`, `DELETE`

#### Example output
```
[
    {
        "id": 5,
        "products": [
            {
                "id": 3,
                "count": 5,
                "product": {
                    "id": 1,
                    "name": "TestProduct0",
                    "price": "0"
                }
            },
            {
                "id": 4,
                "count": 12,
                "product": {
                    "id": 2,
                    "name": "TestProduct1",
                    "price": "1"
                }
            }
        ]
    },
...
```
### Issues

 - Authorization has not been implemented properly via built-in methods, resulting in bad response codes from the server.
 - Built in API tests for some reason doesn't utilise database created for testing purposes, functions work properly on live database. Additional tests were done via Postman, results attached above.

