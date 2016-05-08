#!/usr/bin/env python3

import connexion

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./')
    app.add_api('swagger.yaml')
    app.run(port=8080, debug=True)
