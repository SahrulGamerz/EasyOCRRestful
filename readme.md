# EasyOCR Restful

# Installation

- Clone this repository `git clone https://github.com/SahrulGamerz/EasyOCRRestful`

- Edit `docker-compose.yaml` environment, volume and port

- Edit `build-deploy.sh`, add comment at the front of any optional script

  - Example
  
    - `docker update --cpus 2 --memory 2048M easyocr-restful` to `#docker update --cpus 2 --memory 2048M easyocr-restful`
    
- Run the script `bash build-deploy.sh` or `chmod +x build-deploy.sh && .\build-deploy.sh`

### HTTP Request:

- Method: `POST`

- URL: `http://{server-ip}:2000/ocr`

- Header:

  - Content-Type: application/json

- Request Body:

  - JSON Object with format:

    - `image` - (String) : image url or base64 to be processed
    - `lang` - (String): Language to be used (Optional: Default is `ja`)

  - Example of a payload:

    ```
    {
    	"image": "https://via.placeholder.com/300.jpg?text=Hello_world",
        "lang": "en"
    }
    ```

    _(Placeholder Image above has resolution 300x300px)_

### HTTP Response:

- Status Code: `200` (Success) or `400` if `image` is not given.

- Format: JSON

  - `results` (Array of Object): List of detected texts and rectangle boundary of that text on the source image. Each result object will have format:

    - `coordinate` (Array of Point): Contains 4 points to create rectangle contains the text. Each point is an two value array of float.
    - `score` (Float): The score of the easyocr when detect. From 0 (zero) to 1.
    - `text` (String): Detected text

  - An Example of response data:

    ```json
    {
      "results": [
        {
          "coordinate": [
            [86.0, 138.0],
            [212.0, 138.0],
            [212.0, 170.0],
            [86.0, 170.0]
          ],
          "score": 0.24089430272579193,
          "text": "Hello world"
        }
      ]
    }
    ```

# Credits

https://github.com/voduytuan/Restful-EasyOCR
