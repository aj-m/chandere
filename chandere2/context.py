"""General scraping information related to specific imageboards."""

VICHAN_IMAGE_FIELDS = ("filename", "tim", "ext", "extra_files")
VICHAN_POST_FIELDS = ("no", "time", "name", "trip",
                      "sub", "com", "filename", "ext")

CONTEXTS = {
    "4chan": {"uri": "a.4cdn.org",
              "image_uri": "i.4cdn.org",
              "image_dir": None,
              "board_in_image_uri": True,
              "delimiter": "thread",
              "image_fields": VICHAN_IMAGE_FIELDS,
              "post_fields": VICHAN_POST_FIELDS,
              "reply_field": None},
    "8chan": {"uri": "8ch.net",
              "image_uri": "media.8ch.net",
              "image_dir": "file_store",
              "board_in_image_uri": False,
              "delimiter": "res",
              "image_fields": VICHAN_IMAGE_FIELDS,
              "post_fields": VICHAN_POST_FIELDS,
              "reply_field": None},
    "lainchan": {"uri": "lainchan.org",
                 "image_uri": "lainchan.org",
                 "image_dir": "src",
                 "board_in_image_uri": True,
                 "delimiter": "res",
                 "image_fields": VICHAN_IMAGE_FIELDS,
                 "post_fields": VICHAN_POST_FIELDS,
                 "reply_field": None}
}
