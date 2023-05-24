from api.app import app
from api.globals import settings
import uvicorn


def main():
    uvicorn.run(app, port=settings.port, host='0.0.0.0', access_log=False)


if __name__ == '__main__':
    main()
