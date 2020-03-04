import inspect
import logging

logging.basicConfig(level=logging.INFO)
di_logger = logging.getLogger('di_logger')

class DIContainer(object):

    def __init__(self):
        self._registered_names = set()
        self._factory_funcs = {}
        self._instance_registry = {}
        self._objects_currently_in_creation = set()

    async def on_start_hook(self, app):
        for registered_name in self._registered_names:
            instance = await self.get(registered_name)
            if instance is None:
                raise Exception(f"Registerd function<{registered_name}> returned None")

    def __getattr__(self, attr):
        if attr not in self._instance_registry:
            raise Exception(f"Object is not found with name<{attr}> in registery")
        return self._instance_registry[attr]

    def register(self, name=None):
        def decorator(f):
            register_name = name or self._resolve_name(f)
            dependency_names = self._resolve_dependencies_name(f)

            self._factory_funcs[register_name] = {
                "factory_func": f,
                "dependencies": dependency_names
            }

            self._registered_names.add(register_name)
            di_logger.info(f"Registering <{register_name}> to DI.")
            return f

        return decorator

    def _resolve_name(self, f):
        return f.__name__

    def _resolve_dependencies_name(self, f):
        return list(inspect.signature(f).parameters.keys())

    async def get(self, name):
        if name in self._instance_registry:
            return self._instance_registry[name]

        return await self.create(name)

    async def resolve_dependencies(self, dependency_names, **kwargs):
        dependency_names = dependency_names or []
        params = []
        for parameter in dependency_names:
            if parameter in kwargs:
                params.append(kwargs[parameter])
            else:
                params.append(await self.get(parameter))

        return params

    async def create(self, name):
        if name not in self._factory_funcs:
            raise Exception(f'Dependent object<{name}> not found.')

        if name in self._objects_currently_in_creation:
           reference = "->".join(list(self._objects_currently_in_creation))
           raise Exception(f'Circular Reference detected. {reference}')

        self._objects_currently_in_creation.add(name)

        factory_func_def = self._factory_funcs[name]

        params = await self.resolve_dependencies(factory_func_def.get('dependencies'))

        instance = await self.get_instance(factory_func_def["factory_func"], params)
        self._instance_registry[name] = instance

        return instance

    async def get_instance(self, f, params):
        if inspect.iscoroutinefunction(f):
            return await f(*params)
        else:
            return f(*params)

    async def inject_and_run(self, f, **kwargs):
        parameter_names = self._resolve_dependencies_name(f)
        params = await self.resolve_dependencies(parameter_names, **kwargs)

        if inspect.iscoroutinefunction(f):
            return await f(*params)
        else:
            return f(*params)