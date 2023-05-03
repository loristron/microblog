template = {
  "swagger": "2.0",
  "info": {
    "title": "API Microblog",
    "description": "API de aplicação microblog",
    "version": "1.0.0",
    "contact": {
      "name": "API Microblog",
      "url": "https://loristron.com",
    }
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "Authorization header using the Bearer scheme. Example: \"Bearer YOURCOOLTOKEN\""
    }
  },
  "security": [
    {
      "Bearer": [ ]
    }
  ]
}
