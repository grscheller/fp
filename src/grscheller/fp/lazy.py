# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""### Lazy evaluations.

Delay evaluations until needed or in right scope.

##### Lazy tools:

**lazy:** Delay function evaluation

"""
from __future__ import annotations

__all__ = [ 'Lazy' ]

from typing import Any, Callable, cast, Final, Iterator
from typing import List, Never, overload, Self, Sequence
from .err_handling import MB, XOR
import math


#    __match_args__ = ('_value',)

class Lazy[D, R]():
    """#### Maybe Monad

    Class delaying the executable of a function where `Lazy(f, ds)` constructs
    an object that can evaluate the Callable `f` at a later time. Usually in the
    context of another function call.

    * first argument takes a function of a variable number of arguments
    * takes a tuple of arguments: `tuple[~D, ...]` (`~D` frequently `All`)
    * evaluates the function when the eval method i3 called
    * eval returns: `XOR[tuple[~R, ...], Exception]]` (`~R` frequently `All`)
      * TODO: define Try to wrap such an object???
    * result is cached unless pure is set to false

    """
    __slots__ = '_f', '_args', '_results', '_pure'

    def __init__(self, f: Callable[[D], tuple[R]], *args: D, pure: bool=True) -> None:
        self._f = f
        self._args = args
        self._pure = pure
        self._results: XOR[tuple[R, ...], MB[Exception]] = XOR(right=MB())

    def __bool__(self) -> bool:
        return True if self._results else False

    def eval(self) -> None:
        """Evaluate function with its arguments.

        * evaluate function
        * cache results or exceptions

        """
        if not (self._results and self._pure):
            try:
                result = self._f(*self._args)
            except Exception as exc:
                self._results = XOR(right=MB(exc))
            else:
                if isinstance(result, tuple):
                    self._results = XOR(result, MB())
                elif result is None:
                    results = XOR((), MB())
                else:
                    self._results = XOR((result,), MB())

    def __iter__(self) -> Iterator[R]:
        if not self._results:
            self.eval()
        if self._results:
            for r in self._results.getLeft():
                yield r

    def __call__(self) -> tuple[R, ...]:
        self.eval()
        if self._results:
            return self._results.getLeft()
        else:
            msg = f"lazy: Lazy evaluated function raised exceptions"
            raise RuntimeError(msg)



###

### Grouped exceptions

# def f():
#     excs = [OSError('error 1'), SystemError('error 2')]
#     raise ExceptionGroup('there were problems', excs)
# 

### except*

# def f():
#     raise ExceptionGroup(
#         "group1",
#         [
#             OSError(1),
#             SystemError(2),
#             ExceptionGroup(
#                 "group2",
#                 [
#                     OSError(3),
#                     RecursionError(4)
#                 ]
#             )
#         ]
#     )
# 
# 
# try:
#     f()
# except* OSError as e:
#     print("There were OSErrors")
# except* SystemError as e:
#     print("There were SystemErrors")
# 
# ### adding notes
# 
# try:
#     raise TypeError('bad type')
# except Exception as e:
#     e.add_note('Add some information')
#     e.add_note('Add some more information')
#     raise
# 
# ### instances, not types
# 
# 
# excs = []
# for test in tests:
#     try:
#         test.run()
#     except Exception as e:
#         excs.append(e)
# 
# if excs:
#    raise ExceptionGroup("Test Failures", excs)
# 
# ### 
# 
# def f():
#     raise OSError('operation failed')
# 
# excs = []
# for i in range(3):
#     try:
#         f()
#     except Exception as e:
#         e.add_note(f'Happened in Iteration {i+1}')
#         excs.append(e)