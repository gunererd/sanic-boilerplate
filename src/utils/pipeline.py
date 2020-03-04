class PipelineBuilder(object):

    def __init__(self, di, functions):
        self.di = di
        self.pipeline_executables = []

        for f in functions:
            self.register(f)

    def register(self, func):
        self.pipeline_executables.append({
            "func_name": func.__name__,
            "func": func
        })

    async def execute(self, **kwargs):

        resource = {}
        for executable in self.pipeline_executables:
            func = executable['func']
            resource = await self.di.inject_and_run(func, **kwargs)
            kwargs['resource'] = resource

        return resource
