class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = "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"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}

## Enter your Open API Key here
OPENAI_API_KEY = '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'
