from helpers.logger import setup_logger


class HelloService:
    def __init__(self, config):
        self.logger = setup_logger("app")
        self.constants = config.get("constants", {})

    def say_hello(self):
        self.logger.debug("Processing GET /hello")
        return {"greeting": self.constants.get("greeting_message", "Hello!")}

    def process_data(self, data):
        self.logger.info(f"Processing POST /hello with data: {data}")
        return {
            "received": data,
            "message": self.constants.get("post_ack", "Data received.")
        }
