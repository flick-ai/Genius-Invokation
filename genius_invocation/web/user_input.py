from typing import List
import js
import asyncio

# input
async def get_input(prompt: str, assert_fn=None, dtype=None):
    js.document.getElementById("prompt").innerText = prompt
    while True:
        try:
            user_input = js.document.getElementById("input_result").innerText
            # user_input = input(prompt)
            if dtype is not None:
                user_input = dtype(user_input)
            if assert_fn is not None:
                assert assert_fn(user_input)
            js.document.getElementById("input_result").innerText = ""
            return user_input
        except KeyboardInterrupt:
            exit()
        except:
            js.document.getElementById("error_text").innerText = "您输入的内容无效，请重新输入"
        await asyncio.sleep(0.2)

async def get_sel(prompt: str, selection: List, assert_fn=None, dtype=None):
    '''
    get selection from list
    '''
    while True:
        try:
            if dtype is None:
                dtype = type(selection[0])
            inp = await get_input(prompt, lambda x:x in selection, dtype=dtype)
            if assert_fn is not None:
                assert assert_fn(inp)
            return inp
        except KeyboardInterrupt:
            exit()
        except:
            js.document.getElementById("error_text").innerText = "您输入的内容无效，请重新输入"

async def get_mul_sel(prompt: str, selection: List, assert_fn=lambda x:True):
    '''
    get multiple selections from list
    '''
    while True:
        try:

            raw_input = await get_input(prompt)
            selection = raw_input.split(' ')
            assert len(selection) == len(set(selection))
            for i in selection:
                assert i in selection
            if assert_fn is not None:
                assert assert_fn(selection)
            return selection
        except KeyboardInterrupt:
            exit()
        except:
            js.document.getElementById("error_text").innerText = "您输入的内容无效，请重新输入"

async def get_rng_sel(prompt: str, min=None, max=None, assert_fn=None, dtype=None):
    '''
    get ranged selection
    :param prompt: prompt
    :param min: min value
    :param max: max value
    :param assert_fn: assert function on the input in dtype
    '''
    dtype = str if dtype is None else dtype
    while True:
        try:
            # inp = await get_input(prompt, lambda x: min <= dtype(x) <= max)
            inp = dtype(await get_input(prompt, lambda x: min <= dtype(x) <= max))
            if assert_fn is not None:
                assert assert_fn(inp)
            return
        except KeyboardInterrupt:
            exit()
        except:
            js.document.getElementById("error_text").innerText = "您输入的内容无效，请重新输入"

async def get_rng_mul_sel(prompt: str, min=None, max=None, assert_fn=None, dtype=None):
    '''
    get ranged multiple selection
    :param prompt: prompt
    :param min: min value
    :param max: max value
    :param assert_fn: assert function on the input as a list of dtype
    '''
    dtype = int if dtype is None else dtype
    while True:
        try:
            raw_input = await get_input(prompt)
            selection = raw_input.split(' ')
            assert len(selection) == len(set(selection))
            for i in range(len(selection)):
                selection[i] = dtype(selection[i])
                assert min <= selection[i] <= max
            if assert_fn is not None:
                assert assert_fn(selection)
            return selection
        except KeyboardInterrupt:
            exit()
        except:
            js.document.getElementById("error_text").innerText = "您输入的内容无效，请重新输入"
        await asyncio.sleep(0.2)