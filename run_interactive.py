import time
import re
import logging
from typing import Optional, Union

from df_engine.core.keywords import TRANSITIONS, RESPONSE
from df_engine.core import Context, Actor
import df_engine.conditions as cnd
from scenario.main import actor


 

## turn_handler - a function is made for the convenience of working with an actor
def turn_handler(
    in_request: str, ctx: Union[Context, str, dict], actor: Actor, true_out_response: Optional[str] = None
):
    # Context.cast - gets an object type of [Context, str, dict] returns an object type of Context
    ctx = Context.cast(ctx)
    # Add in current context a next request of user
    ctx.add_request(in_request)
    # pass the context into actor and it returns updated context with actor response
    ctx = actor(ctx)
    # get last actor response from the context
    out_response = ctx.last_response
    # the next condition branching needs for testing
    if true_out_response is not None and true_out_response != out_response:
        msg = f"in_request={in_request} -> true_out_response != out_response: {true_out_response} != {out_response}"
        raise Exception(msg)
    else:
        logging.info(f"in_request={in_request} ->\n {out_response}")
    return out_response, ctx



def run_interactive_mode(actor):
    ctx = {}
    while True:
        in_request = input("type your answer: ")
        st_time = time.time()
        _, ctx = turn_handler(in_request, ctx, actor)
        total_time = time.time() - st_time
        print(f"exec time = {total_time:.3f}s")



if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s-%(name)15s:%(lineno)3s:%(funcName)20s():%(levelname)s - %(message)s", level=logging.INFO
    )
    
#     run_test()
    run_interactive_mode(actor)
