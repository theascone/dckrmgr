import os
import json
import jsonschema

def read_json(pth, sch=None):
    bsn = os.path.basename(pth)

    try:
        f_jsn = open(pth, 'r')
    except FileNotFoundError:
        print('Couldn\'t open ' + bsn + ': Not found')
        exit(1)
    except PermissionError:
        print('Couldn\'t open ' + bsn + ': Insufficient rights')
        exit(1)
    except OSError:
        print('Couldn\'t open ' + bsn)
        exit(1)

    try:
        jsn = json.load(f_jsn)
    except ValueError:
        print('Couldn\'t deserialize ' + bsn + ': Invalid json')
        exit(1)
    finally:
        f_jsn.close()

    if sch is not None:
        try:
            jsonschema.validate(jsn, sch)
        except jsonschema.exceptions.SchemaError:
            print('Couldn\'t validate ' + bsn + ': Invalid schema')
            exit(1)
        except jsonschema.exceptions.ValidationError as error:
            print('Couldn\'t accept '+ bsn + ': ' + error.message)
            exit(1)

    return jsn
