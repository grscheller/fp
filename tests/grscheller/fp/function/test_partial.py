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
# See the License for the specific language governing permissions anddd
# limitations under the License.

from grscheller.fp.function import partial

class Test_partial:
    def test_same_type(self) -> None:
        def multAdd(m1: int, m2: int, a: int) -> int:
            return m1*m2 + a

        ans = 8*5 + 2
        assert ans == multAdd(8, 5, 2)

        p1 = partial(multAdd, 8)
        p2 = partial(multAdd, 8, 5)
        p3 = partial(multAdd, 8, 5, 2)

        assert p1(5, 2) == p2(2) == p3() == ans

