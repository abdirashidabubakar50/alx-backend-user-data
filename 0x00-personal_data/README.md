## Loggin facility for Python

This module defines functions and classes which implementa a flexbile event logging system for application and libraries

The key benefit of having the logging API is that all python modules can participate in logging, so your application include your messages integrated with messages form third-party modules

example of an idiomatic Usage
- ```
    import logging
    logger = logging.getLogger(__name__)

    def do_something():
        logger.info('Doing something')

    def main():
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        logger.info('Started')
        do_something()
        logger.info('Finished')

    if __name__ == '__main__':
        main()
  ```
The output of this code should appear in myapp.log looking like this:

    INFO:__main__:Started
    INFO:mylib:Doing something
    INFO:__main__:Finished


The key feature of this idiomatic usage is that the majority of the code is simply creating a module level logger ith getLogger(__name__), and using that logger to do any needed logging.