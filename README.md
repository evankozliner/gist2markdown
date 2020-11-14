# gist2markdown
Simply converts a gist to markdown with the correct language. 


## Usage

```
$ python gist2markdown.py -h
usage: gist2markdown.py [-h] -u URL [-d]

Prints markdown based on some gist url.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The gist URL to pull from.
  -d, --follow-redirects
                        Follow redirects when pulling URL. Useful for sites
                        that redirect to github, but place the URL under their
                        own domain, like Medium.
```


### Example

```
$ python gist2markdown.py  -u https://medium.com/media/f9bfd1bd783061d25f84afd11564d8c0 
Found gist ID f2e0c4eb5cd6d15fdfc8ca6cdd9d8bb5
```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:CreateUser"
            ],
            "Resource": [
                "arn:aws:iam::123456789012:role/some-role",
                "arn:aws:iam::123456789012:user/some-user"
            ]
        },
        {
            "Action": [
                "logs:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
\```

```

I manually added the final backslash above just to get this README, which is also in markdown, to not break formatting.


### Example 2
```
$ python gist2markdown.py  --url https://gist.githubusercontent.com/evankozliner/f0cba2cdad0afa4ca50c293256bf7b79/raw/2eaa6b93040b1c501e2c37c7899b28a1f9b965e9 >> ec2-role.md
$ cat ec2-role.md 
Found gist ID f0cba2cdad0afa4ca50c293256bf7b79
```JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEC2",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "AllowAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::123456789012:role/devops",
          "arn:aws:iam::123456789012:role/jenkins-master"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
\``` 

```

### Example 3

It can handle multiple files too

```
$ python gist2markdown.py  --url https://gist.github.com/evankozliner/0884837e6835e8b951f0e2e4ce4d6042                                                            
Found gist ID 0884837e6835e8b951f0e2e4ce4d6042
```Python
import re
import argparse
import requests

def main():
    args = parse_args()

    gist_id = find_id(args.url, args.follow_redirects)
    print(f"Found gist ID {gist_id}")
    gist_api_adaptor = GistAPIAdaptor(gist_id)
    gist_api_adaptor.fetch()
    file_types = gist_api_adaptor.get_file_langs()
    raw_urls =  gist_api_adaptor.get_raw_urls()
    for i in range(len(raw_urls)):
        output_markdown(file_types[i], raw_urls[i])


\```
```JSON
{
  "some-key": 2
}


\```
```


