import base64

class Solver:
    def __init__(self, code):
        self.code = code

    def decode(self, base64_message):
        try:
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            return message
        except Exception as e:
            return None

    def getCode(self):
        previous_code = None
        while True:
            decoded_code = self.decode(self.code)
            if decoded_code is None:
                return previous_code
            previous_code = decoded_code
            self.code = decoded_code

    def encode(self, times):
        if times <= 0:
            raise ValueError("Times must be a positive integer.")
        
        encoded_code = self.code
        for i in range(times):
            encoded_code = self.encode_once(encoded_code)
        return encoded_code

    def encode_once(self, message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

