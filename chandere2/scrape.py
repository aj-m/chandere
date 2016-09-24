# """[Document me!]"""

# import asyncio

# from chandere2.connection import fetch_uri


# async def scrape_targets(target_uris: list, use_ssl: bool, output):
#     failed_uris = []
    
#     for uri in target_uris:
#         fetch = fetch_uri(uri, target_uris[uri][2], use_ssl, output)
#         response, error, last_load = await fetch

#         if not error and response:
#             print(response) ## placeholder
#             target_uris[uri][2] = last_load
#         elif error:
#             failed_uris.append(uri)

#     for uri in failed_uris:
#         del target_uris[uri]
