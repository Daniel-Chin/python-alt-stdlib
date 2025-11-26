'''
Automatic retry of OpenAI GPT calls.  
Deprecated in favor of tenacity.  
'''

from typing import Callable
import time

import openai

def callWithAutoRetry(callable: Callable, *a, **kw):
    retry_i = 0
    max_retry = 4
    while retry_i < max_retry:
        try:
            return callable(*a, **kw)
        except (
            openai.BadRequestError, 
            openai.AuthenticationError, 
            openai.PermissionDeniedError, 
            openai.NotFoundError, 
            openai.ConflictError, 
            openai.UnprocessableEntityError, 
        ) as e:
            raise e
        except openai.RateLimitError as e:
            print(e)
            to_sleep = ((retry_i + 1) / 2) ** 2
            print(f'Retrying in {to_sleep} seconds.')
            time.sleep(to_sleep)
            print('Retrying...')
            continue
        except openai.InternalServerError as e:
            print(e)
            to_sleep = 1
            print(f'Retrying in {to_sleep} seconds.')
            time.sleep(to_sleep)
            print('Retrying...')
            continue
        except Exception as e:
            raise e
        finally:
            retry_i += 1
    else:
        raise RuntimeError('Too many retries.')
