class Entity:
    def render(self):
        """A central method to Synthesium. Allows an VectorEntity to render itself."""
        pass


def configure(default_config, **kwargs):
    """Configure works by taking in all the kwargs passed to init(), and comparing them against the default config. Anything new is updated,
       otherwise the defaults are used. This allows for the dynamic setting of attributes in one dictionary."""
    new_config = kwargs
    for key, value in new_config.items():
        default_config[key] = value  # update the default_config as necessary with new values
    return default_config  # while it returns "default_config," it's really returning the modified config.
