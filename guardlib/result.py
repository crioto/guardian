# Result class represents test results in YAML format

import yaml

class Result:
    componentName = "unnamed"
    testName = "unnamed"
    timestamp = 0
    statusCode = -1
    peerId = "unknown"
    fields = {}

    def __init__(self, component, test, statusCode):
        self.componentName = component
        self.testName = test


    # append will add additional property to the report
    def append(self, name, value):
        self.fields.update({name: value})


    # build will generate YAML-encoded data
    def build(self):
        data = {
            "component": self.componentName,
            "name": self.testName
        }
        if len(self.fields) > 0:
            payload = {}
            for n, v in self.fields.items():
                payload[n] = v

            data["payload"] = payload

        res = yaml.dump(data)
        return res