# Image Processing Api

## To Run the Project:
```
mv .env.example .env
```
* change the content of .env file
```
docker compose up --build
```

## Storage Options:
### The app supports 2 types of image storage in the database: 
* as a file path (default one, and it is done regardless of the specified storage type)
  - Input imgages: /images/input/
  - Output images: /images/output/ 
* in the base64 string form 

## Supported Input Types:
* multipart/form-data format, where the user sends images via form submissions and add operations (text field) which is in the json format and then converted to json
* base64 string format, where user sends images and corressponding operations altogether   

## Endpoints:
* POST: /images/process
* GET: /images (to retrieve images in the base64 form takes absolute path string as input)

## To Run on Postman
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/33741357-7b8209cf-33a9-4dcf-bf29-aa2bd4114373?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33741357-7b8209cf-33a9-4dcf-bf29-aa2bd4114373%26entityType%3Dcollection%26workspaceId%3Dfae1ec64-8bc6-4763-a391-fe8e5712a08a)

## JSON Payload Examples:
### For Form Format:
```
{
  "storage": "database",
  "operations": [
    {
      "filename": "",
      "format": "",
      "directives": [
        { 
        "operation": "resize", 
        "parameters": { 
            "width": 400,
            "height": 300,
            "mode": "exact"
        } 
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "rotate", 
        "parameters": { 
            "angle": 90
        } 
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "grayscale"
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "channel_conversion",
        "parameters": {
            "channel": "RGB",
            "to": "BGR"
        }
        }
      ]
    }
  ]
}
``` 
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "perspective_transformation",
        "parameters": {
            "source": [[0,0], [0,0], [0,0], [0,0]],
            "destination": [[0,0], [0,0], [0,0], [0,0]]
        }
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "compress",
        "parameters": {
            "quality": 0
        }
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "format_conversion",
        "parameters": {
            "target": "jpg"
        }
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
        { 
        "operation": "draw",
        "parameters": {
            "dots": [
                {
                    "position": [x, y],
                    "color": [r, g, b]
                }
            ]
            
            "rectangles": [
                {
                    "position": [x, y],
                    "size": sz,
                    "color": [r, g, b],
                    "thickness": t
                }
            ]
            
            "circles": [
                {
                    "center": [x, y],
                    "radius": r,
                    "color": [r, g, b],
                    "thickness": t
                }
            ]
        }
        }
      ]
    }
  ]
}
```
```
{
  "operations": [
    {
      "directives": [
      ]
    },
    {
      "directives": [
      ]
    }
  ],
    
  "gif": {
    "generate": true,
    "frame_interval": 1
  }
}
```

### For Base64 Format:
```
{
  "storage": "",
  "images": [
    {
      "filename": "",
      "format": "",
      "directives": [
        {
          "operation": "",
          "parameters": {
          
          }
        }
      ],
      "data": ""
    }
  ],
  "gif": {
    "generate": true,
    "frame_interval": 1
  }
}
```

## Schemas:
### Operation
* operation: string (indicating operation type)
* parameters: dictionary

### ImageMetadata
* filename: string
* format: string
* directives: List[Operation]

### Image (extends ImageMetaData)
* data: string (for base64 strings)

### GifParameters (since I treat gif generation differently)
* generate: bool
* frame_interval: int (seconds)

### Base64Format
* storage: string 
* images: List[Image]
* gif: GifParameters

### FormFormat
* storage: string 
* gif: GifParameters
* operations: Listp[ImageMetadata]

