from typing import Any, Iterator, Self, TypedDict
from types import NotImplementedType

# Паттерн Моносостояние/mono_state


class SharedAttrs(TypedDict):
    id: int
    name: str
    age: int
    date: dict[str, int]


class MonoState:
    __shared_attrs: SharedAttrs = {
        "id": 0,
        "name": "",
        "age": 0,
        "date": {},
    }

    def __init__(self) -> None:
        self.__dict__ = dict(self.__shared_attrs)


# --


class CExample:
    """Main demonstration class for (magic) dunder methods"""

    # -- Создание и жизненный цикл

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # *
        """
        Метод создания объекта.

        __new__ вызывается ПЕРВЫМ при создании экземпляра класса,
        ещё до __init__.

        Основная задача __new__:
        - создать объект в памяти
        - вернуть экземпляр класса

        Последовательность создания объекта:

            obj = C(1, 2)

        Внутри Python примерно:

            obj = C.__new__(C, 1, 2)

            if isinstance(obj, C):
                C.__init__(obj, 1, 2)

        Важно:
        - __new__ СОЗДАЁТ объект
        - __init__ ИНИЦИАЛИЗИРУЕТ объект

        Аргумент cls:
        - cls — ссылка на сам класс
        - через cls Python понимает объект какого
        класса необходимо создать

        super().__new__(cls):
        - вызывает object.__new__(cls)
        - выделяет память под новый объект
        - создаёт "пустой" экземпляр класса

        Примерно внутри CPython:

            allocate_memory()
            create_pyobject()
            return instance

        Если __new__ НЕ вернуть экземпляр класса,
        то __init__ вызван НЕ будет.

        Например:

            def __new__(cls):
                return 123

        Тогда объект класса вообще не создастся.

        __new__ обычно используют редко.
        Основные сценарии:
        - singleton pattern
        - immutable objects
        - metaprogramming
        - object caching
        - custom instance creation
        - inheritance control

        Особенно важен __new__ для immutable типов:
        - str
        - tuple
        - int

        Потому что immutable объект нельзя изменить
        после создания, значит все данные должны быть
        подготовлены именно в __new__.

        Внутри CPython создание объекта связано с:
            type.__call__()
                ↓
            cls.__new__()
                ↓
            cls.__init__()

        То есть когда вызывается:

            C()

        Python фактически делает:

            type(C).__call__(C)

        А внутри type.__call__ уже вызываются
        __new__ и __init__.
        """

        print("__new__ called", end="\n")

        # Создание пустого экземпляра класса
        instance = super().__new__(cls)

        return instance

    def __init__(self, name: str, age: int, value: int) -> None:  # *
        """
        Инициализатор объекта.

        Метод автоматически вызывается после создания объекта
        через __new__.

        Основная задача __init__:
        - инициализация состояния объекта
        - создание атрибутов экземпляра
        - подготовка объекта к работе

        Последовательность создания объекта:

            obj = C(1, 2)

        Внутри Python примерно:

            obj = C.__new__(C, 1, 2)

            if isinstance(obj, C):
                C.__init__(obj, 1, 2)

        Важно:
        - __init__ НЕ создаёт объект.
        - Объект уже существует к моменту вызова __init__.
        - За создание объекта отвечает __new__.

        Аргумент self:
        - self — ссылка на уже созданный экземпляр класса.
        - Через self происходит запись атрибутов в объект.

        Пример:

            self.arg_1 = arg_1

        означает:

            object.__setattr__(self, "arg_1", arg_1)

        __init__ должен возвращать None.
        Возврат любого другого значения вызовет TypeError.

        Обычно внутри __init__:
        - создают атрибуты
        - валидируют данные
        - подготавливают зависимости
        - инициализируют внутреннее состояние объекта
        """

        print("__init__ called", end="\n")

        self.name = name
        self.age = age
        self.value = value

    def __del__(self) -> None:
        """
        Финализатор объекта.

        Метод вызывается интерпретатором Python перед уничтожением
        объекта, когда reference count объекта становится равен нулю
        или объект удаляется garbage collector'ом.

        Важно:
        - del obj НЕ удаляет объект напрямую.
        - del obj удаляет только ссылку/имя.
        - __del__ вызывается только тогда, когда на объект
        больше не остаётся ссылок.

        Пример:

            a = C()
            b = a

            del a

        В этом случае __del__ НЕ вызовется,
        потому что объект всё ещё доступен через b.

        Метод обычно используют для:
        - debug/logging
        - cleanup low-level ресурсов
        - weakref/finalizer logic

        Не рекомендуется использовать __del__
        для критически важного освобождения ресурсов,
        потому что Python НЕ гарантирует точный момент вызова.

        Для cleanup лучше использовать:
        - context managers
        - try/finally
        - with statement

        Внутри CPython вызов происходит через:
            tp_dealloc -> __del__ -> free memory
        """

        print("__del__ call", end="\n")

    # -- Строковое представление

    def __str__(self) -> str:  # *
        """
        Человекочитаемое строковое представление объекта.

        Вызывается:
        - print(obj)
        - str(obj)
        - f"{obj}"

        Предназначен для:
        - пользователя
        - красивого вывода
        - UI/logging

        Должен возвращать строку.
        Если __str__ НЕ определён,
        Python использует __repr__.
        Пример:
            print(obj)
        Внутри Python примерно:
            result = obj.__str__()
        """

        print("__str__ called", end="\n")

        return f"{self.name} {self.age} "

    def __repr__(self) -> str:  # *
        """
        Строковое представление объекта для разработчика.

        Вызывается:
        - repr(obj)
        - obj в REPL/console
        - logging/debugging
        - list/dict/set printing

        Предназначен для:
        - debugging
        - internal representation
        - developer output

        В идеале repr должен быть:
        - однозначным
        - информативным
        - по возможности executable

        Хорошая практика:
            repr(obj)

        должен позволять понять:
        - тип объекта
        - состояние объекта

        Пример:
            C(name='Alex', age=20)

        Если __repr__ НЕ определён,
        Python использует object.__repr__:
            <__main__.CExample object at 0x...>

        Внутри Python
            result = obj.__repr__()

        """

        print("__repr__ called", end="\n")

        return f"CExample(name={self.name}, age={self.age})"

    def __format__(self, format_spec: str) -> str:
        """
        Кастомное форматирование объекта.
        Вызывается:

        - format(obj, spec)
        - f"{obj:spec}"

        format_spec:
        - строка формата после ':'

        Пример:
            f"{obj:short}"
        Тогда:
            format_spec == "short"

        Используется для:
        - кастомного отображения
        - отчётов
        - pretty-printing
        - table rendering

        Если __format__ НЕ определён,
        Python использует str(obj).
        Внутри Python:
            result = obj.__format__(format_spec)
        """

        print("__format__ called", end="\n")

        if format_spec == "short":
            return self.name

        if format_spec == "full":
            return f"{self.name} {self.age}"

        return str(self)

    def __bytes__(self) -> bytes:
        """
        Бинарное представление объекта.

        Вызывается:
        - bytes(obj)

        Должен возвращать bytes.
        Используется для:
        - serialization
        - networking
        - binary protocols
        - file IO
        - encoding

        Внутри Python:
            result = obj.__bytes__()

        Обычно объект переводят:
        - в UTF-8
        - JSON
        - binary payload

        Если вернуть НЕ bytes,
        Python выбросит TypeError.
        """

        print("__bytes__ called", end="\n")

        return f"{self.name}:{self.age}".encode("utf-8")

    # -- Сравнение

    def __eq__(
        self, other: object
    ) -> bool | NotImplementedType:  # * Остальное инвертируется
        """
        Перегрузка оператора сравнения ==.

        Вызывается при:
            obj == other

        Python внутри делает:
            obj.__eq__(other)

        Аргументы:
        - self:
            текущий объект

        - other:
            объект для сравнения (любой тип)

        Возвращает:
        - bool:
            результат сравнения

        Важно:
        - должен возвращать True / False
        - может вернуть NotImplemented, если типы несовместимы

        Тогда Python попробует:
        - reversed comparison
        - или fallback поведение
        """

        if not isinstance(other, CExample):
            return NotImplemented

        return self.value == other.value

    def __ne__(
        self, other: object
    ) -> bool | NotImplementedType:  # * Остальное инвертируется
        """
        Перегрузка оператора !=.

        Вызывается при:
            obj != other

        Python внутри делает:
            obj.__ne__(other)

        Аргументы:
        - self:
            текущий объект

        - other:
            объект для сравнения

        Возвращает:
        - bool
        - либо NotImplemented

        Обычно логика __ne__ противоположна __eq__.
        Если вернуть NotImplemented,
        Python попробует fallback comparison.
        """

        if not isinstance(other, CExample):

            return NotImplemented

        return self.value != other.value

    def __lt__(
        self, other: object
    ) -> bool | NotImplementedType:  # * Остальное инвертируется
        """
        Перегрузка оператора <.
        Вызывается при:
            obj < other

        Python внутри делает:
            obj.__lt__(other)

        Аргументы:
        - self:
            текущий объект
        - other:
            объект для сравнения

        Возвращает:
        - bool
        - либо NotImplemented

        Используется для:
        - сортировки
        - сравнения
        - ordering logic

        Важно:
        other должен быть object,
        потому что Python может сравнить
        объект с чем угодно.

        Если тип несовместим,
        правильно вернуть:
            NotImplemented

        Тогда Python попробует:
        - reverse comparison
        - fallback behavior
        """

        if not isinstance(other, CExample):
            return NotImplemented

        return self.value < other.value

    def __le__(
        self, other: object
    ) -> bool | NotImplementedType:  # * Остальное инвертируется
        """
        Перегрузка оператора <=.
        Вызывается при:
            obj <= other

        Python внутри делает:
            obj.__le__(other)

        Возвращает:
        - bool
        - либо NotImplemented
        """

        if not isinstance(other, CExample):
            return NotImplemented

        return self.value <= other.value

    def __gt__(self, other: object) -> bool | NotImplementedType:
        """
        Перегрузка оператора >.
        Возвращает True, если self.value больше other.value или другого числа.
        """

        if not isinstance(other, CExample):
            return NotImplemented

        return self.value > other.value

    def __ge__(self, other: object) -> bool | NotImplementedType:
        """
        Перегрузка оператора >=.
        """

        if not isinstance(other, CExample):
            return NotImplemented

        return self.value >= other.value

    # -- Арифметика

    def __add__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора +.

        Поддерживает сложение с другим CExample или числом.
        """

        if isinstance(other, CExample):
            return self.value + other.value

        if isinstance(other, (int, float)):
            return self.value + other

        return NotImplemented

    def __sub__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора -.
        """

        if isinstance(other, CExample):
            return self.value - other.value

        if isinstance(other, (int, float)):
            return self.value - other

        return NotImplemented

    def __mul__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора *.
        """

        if isinstance(other, CExample):
            return self.value * other.value

        if isinstance(other, (int, float)):
            return self.value * other

        return NotImplemented

    def __truediv__(self, other: object) -> float | NotImplementedType:
        """
        Перегрузка оператора /.
        """

        if isinstance(other, CExample):
            return self.value / other.value

        if isinstance(other, (int, float)):
            return self.value / other

        return NotImplemented

    def __floordiv__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора //.
        """

        if isinstance(other, CExample):
            return self.value // other.value

        if isinstance(other, (int, float)):
            return self.value // other

        return NotImplemented

    def __mod__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора %.
        """

        if isinstance(other, CExample):
            return self.value % other.value

        if isinstance(other, (int, float)):
            return self.value % other

        return NotImplemented

    def __pow__(self, other: object) -> int | float | NotImplementedType:
        """
        Перегрузка оператора **.
        """

        if isinstance(other, CExample):
            return self.value**other.value

        if isinstance(other, (int, float)):
            return self.value**other

        return NotImplemented

    # -- Reverse арифметика

    def __radd__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное сложение.
        """

        if isinstance(other, (int, float)):
            return other + self.value

        return NotImplemented

    def __rsub__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное вычитание.
        """

        if isinstance(other, (int, float)):
            return other - self.value

        return NotImplemented

    def __rmul__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное умножение.
        """

        if isinstance(other, (int, float)):
            return other * self.value

        return NotImplemented

    def __rtruediv__(self, other: object) -> float | NotImplementedType:
        """
        Обратное деление.
        """

        if isinstance(other, (int, float)):
            return other / self.value

        return NotImplemented

    def __rfloordiv__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное целочисленное деление.
        """

        if isinstance(other, (int, float)):
            return other // self.value

        return NotImplemented

    def __rmod__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное вычисление остатка.
        """

        if isinstance(other, (int, float)):
            return other % self.value

        return NotImplemented

    def __rpow__(self, other: object) -> int | float | NotImplementedType:
        """
        Обратное возведение в степень.
        """

        if isinstance(other, (int, float)):
            return other**self.value

        return NotImplemented

    # -- Inplace арифметика

    def __iadd__(self, other: object) -> Self:
        """
        += с модификацией self.
        """

        if isinstance(other, CExample):
            self.value += other.value
        elif isinstance(other, (int, float)):
            self.value += other
        else:
            return NotImplemented

        return self

    def __isub__(self, other: object) -> Self:
        """
        -= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value -= other.value
        elif isinstance(other, (int, float)):
            self.value -= other
        else:
            return NotImplemented

        return self

    def __imul__(self, other: object) -> Self:
        """
        *= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value *= other.value
        elif isinstance(other, (int, float)):
            self.value *= other
        else:
            return NotImplemented

        return self

    def __itruediv__(self, other: object) -> Self:
        """
        /= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value /= other.value
        elif isinstance(other, (int, float)):
            self.value /= other
        else:
            return NotImplemented

        return self

    def __ifloordiv__(self, other: object) -> Self:
        """
        //= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value //= other.value
        elif isinstance(other, (int, float)):
            self.value //= other
        else:
            return NotImplemented

        return self

    def __imod__(self, other: object) -> Self:
        """
        %= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value %= other.value
        elif isinstance(other, (int, float)):
            self.value %= other
        else:
            return NotImplemented

        return self

    def __ipow__(self, other: object) -> Self:
        """
        **= с модификацией self.
        """

        if isinstance(other, CExample):
            self.value **= other.value
        elif isinstance(other, (int, float)):
            self.value **= other
        else:
            return NotImplemented

        return self

    # -- Унарные операции

    def __neg__(self) -> int | float:
        """
        Унарный минус.
        """

        return -self.value

    def __pos__(self) -> int | float:
        """
        Унарный плюс.
        """

        return +self.value

    def __invert__(self) -> int:
        """
        Битовая инверсия.
        """

        return ~int(self.value)

    # -- Преобразование типов

    def __int__(self) -> int:
        """
        Приведение к int.
        """

        return int(self.value)

    def __float__(self) -> float:
        """
        Приведение к float.
        """

        return float(self.value)

    def __bool__(self) -> bool:
        """
        Приведение к bool.
        """

        return bool(self.value)

    def __complex__(self) -> complex:
        """
        Приведение к complex.
        """

        return complex(self.value)

    def __index__(self) -> int:
        """
        Возвращает целочисленный индекс объекта.
        """

        return int(self.value)

    # -- Контейнеры

    def __len__(self) -> int:
        """
        Перегрузка встроенной функции len().

        Вызывается при:
            len(obj)

        Python внутри делает:
            obj.__len__()

        Метод должен вернуть неотрицательное
        целое число (int), которое интерпретируется
        как размер, длина или количество элементов
        объекта.

        Используется для:
        - коллекций
        - контейнеров
        - последовательностей
        - пользовательских структур данных

        Примеры:
            len(list)
            len(dict)
            len(str)
            len(set)

        Все они внутри используют __len__().
        Важно:
        - результат должен быть int
        - результат должен быть >= 0

        Если вернуть:
            str
            float
            list
            другой объект
        Python выбросит TypeError.

        Если вернуть отрицательное число:
            return -1
        Python выбросит ValueError.

        Дополнительно:
        bool(obj) по умолчанию использует __len__,
        если __bool__ не определён.

        То есть:
            if obj:
        может внутри превратиться в:
            len(obj) != 0
        если метод __bool__ отсутствует.

        Пример:
            class Basket:

                def __len__(self) -> int:
                    return 3

            basket = Basket()

            len(basket)  # 3
        """

        return len(self.__dict__)  # Мы сами определяем что вернуть

    def __contains__(self, item: object) -> bool:
        """
        Проверяет наличие ключа в атрибутах экземпляра.
        """

        return isinstance(item, str) and item in self.__dict__

    def __getitem__(self, key: str) -> Any:
        """
        Доступ к значению по ключу атрибута.
        """

        if not isinstance(key, str):
            raise TypeError("Keys must be strings")

        return self.__dict__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Устанавливает значение по ключу атрибута.
        """

        if not isinstance(key, str):
            raise TypeError("Keys must be strings")

        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Удаляет атрибут по ключу.
        """

        if not isinstance(key, str):
            raise TypeError("Keys must be strings")

        del self.__dict__[key]

    def __reversed__(self) -> Iterator[tuple[str, Any]]:
        """
        Возвращает итератор по атрибутам в обратном порядке.
        """

        return reversed(tuple(self.__dict__.items()))

    def __iter__(self) -> Iterator[str]:
        """
        Возвращает итератор по именам атрибутов.
        """

        self._iterator_keys = list(self.__dict__.keys())
        self._iterator_index = 0
        return self

    def __next__(self) -> str:
        """
        Возвращает следующий атрибут для итерации.
        """

        try:
            key = self._iterator_keys[self._iterator_index]
        except AttributeError:
            self._iterator_keys = list(self.__dict__.keys())
            self._iterator_index = 0
            key = self._iterator_keys[self._iterator_index]
        except IndexError:
            raise StopIteration

        self._iterator_index += 1
        return key

    # -- Атрибуты

    def __getattr__(self, item: str) -> Any:
        """
        Перехват обращения к НЕСУЩЕСТВУЮЩЕМУ атрибуту.

        Вызывается только если Python НЕ смог
        найти атрибут через стандартный механизм
        поиска внутри __getattribute__.

        Последовательность поиска:

        1. __getattribute__()
        2. instance __dict__
        3. class attributes
        4. MRO lookup
        5. descriptors
        6. __getattr__()

        То есть __getattr__ — это fallback handler.

        Пример:

            obj.name

        Python внутри делает:

            obj.__getattribute__("name")

        Если возникает:

            AttributeError

        тогда вызывается:

            obj.__getattr__("name")

        Важно:
        - __getattribute__ вызывается ВСЕГДА
        - __getattr__ только если атрибут НЕ найден

        Аргументы:
        - self:
            экземпляр объекта

        - item:
            имя отсутствующего атрибута

        Метод должен:
        - вернуть значение
        - либо выбросить AttributeError

        Используется для:
        - dynamic attributes
        - lazy loading
        - proxy objects
        - ORM internals
        - API wrappers
        - fallback logic
        - compatibility layers

        Пример динамического атрибута:

            obj.user_1

        можно обработать программно:

            if item.startswith("user_"):
                return load_user(item)

        Важно:
        внутри нельзя делать:

            self.some_attr

        без super/object.__getattribute__,
        иначе можно получить рекурсию.

        Обычно __getattr__ используют
        для виртуальных атрибутов.

        Пример:

            class C:

                def __getattr__(self, item):
                    return "default"

            obj = C()

            print(obj.anything)

        Результат:
            default
        """

        print(f"Attribute '{item}' not found")
        return f"default value for '{item}'"

    def __getattribute__(self, item: str) -> Any:
        """
        Низкоуровневый перехват доступа к атрибутам объекта.
        Вызывается АБСОЛЮТНО ВСЕГДА при обращении
        к любому атрибуту:
            obj.name
            obj.method
            obj.__dict__
            obj.__class__

        Python внутри делает:
            obj.__getattribute__("name")

        Это основной механизм доступа к атрибутам
        в object model Python.

        Аргументы:
        - self:
            экземпляр объекта
        - item:
            имя запрашиваемого атрибута

        Метод должен:
        - вернуть значение атрибута
        - либо выбросить AttributeError

        Если внутри НЕ вызвать:
            super().__getattribute__(item)
        то стандартный механизм поиска атрибутов
        работать не будет.

        Поиск атрибутов внутри object.__getattribute__:
        1. data descriptors
        2. instance __dict__
        3. class attributes
        4. MRO lookup
        5. non-data descriptors
        6. __getattr__

        Важно:
        внутри нельзя обращаться к атрибутам через:
            self.name

        потому что это снова вызовет:
            __getattribute__()
        и приведёт к бесконечной рекурсии.

        Правильно:
            super().__getattribute__(item)
        или:
            object.__getattribute__(self, item)

        Используется для:
        - proxy objects
        - lazy loading
        - ORM internals
        - logging/tracing
        - access control
        - dynamic attributes
        - framework internals

        Разница:
        - __getattribute__ вызывается ВСЕГДА
        - __getattr__ только если атрибут не найден"""

        print(f"Getting attribute -> {item}")
        # object.__getattribute__(self, item)
        return super().__getattribute__(item)

    def __setattr__(self, key: str, value: Any) -> None:  # *
        """
        Низкоуровневый перехват установки атрибутов.
        Вызывается при ЛЮБОМ присваивании:
            obj.name = "Alex"

        Python внутри делает:
            obj.__setattr__("name", "Alex")

        Аргументы:
        - self:
            экземпляр объекта
        - key:
            имя атрибута
        - value:
            значение атрибута

        Метод отвечает за запись атрибутов
        в объект.
        Если внутри НЕ вызвать:
            super().__setattr__(key, value)
        атрибут реально записан не будет.

        Важно:
        внутри нельзя делать:
            self.name = value
        потому что это снова вызовет:
            __setattr__()
        и приведёт к бесконечной рекурсии.
        Правильно:
            super().__setattr__(key, value)
        или:
            object.__setattr__(self, key, value)

        Используется для:
        - validation
        - ORM internals
        - immutable objects
        - descriptors
        - logging
        - access control
        - reactive objects
        - framework internals

        Пример:
            self.age = -1

        можно перехватить и запретить:
            if value < 0:
                raise ValueError
        """

        print(f"Setting {key} = {value}")
        super().__setattr__(key, value)

    def __delattr__(self, item: str) -> None:
        """

        Перехват удаления атрибута объекта.
        Вызывается при:
            del obj.attr

        Python внутри делает:
            obj.__delattr__("attr")

        Используется для:
        - logging
        - access control
        - validation
        - ORM internals
        - proxy objects

        Важно:
        внутри нельзя делать:
            del self.attr
        Иначе будет рекурсия.

        Правильно:
            super().__delattr__(item)

        Пример:
            del obj.name
        ↓
            obj.__delattr__("name")
        """

        print(f"Deleting attribute -> {item}")

        super().__delattr__(item)

    def __dir__(self) -> list[str]:
        """
        Кастомизация dir(obj).
        Вызывается при:
            dir(obj)

        Python внутри делает:
            obj.__dir__()

        Метод должен вернуть список строк
        с именами атрибутов.

        Используется для:
        - autocomplete
        - IDE support
        - dynamic APIs
        - proxy objects
        - hiding internals

        По умолчанию Python:
        - собирает instance attrs
        - class attrs
        - attrs из MRO

        Но через __dir__ можно полностью
        переопределить поведение.
        Например скрыть внутренние атрибуты
        или добавить виртуальные.
        Важно:
        метод должен вернуть iterable строк.
        Обычно:
            list[str]
        """

        default_attrs: list[str] = list(super().__dir__())
        custom_attrs: list[str] = [
            "virtual_attr",
            "dynamic_method",
        ]

        return default_attrs + custom_attrs

    # -- Вызов объекта

    def __call__(self, *args: Any, **kwargs: Any) -> str:
        """
        Обеспечивает возможность вызова экземпляра как функции.

        Пример:
            obj()
        """

        if args or kwargs:
            return f"{self.name} called with args={args} kwargs={kwargs}"

        return f"{self.name} called"

    # -- Context manager

    def __enter__(self) -> Self:
        """
        Вход в контекстный менеджер.

        Возвращает сам объект.
        """

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> bool:
        """
        Выход из контекстного менеджера.

        Возвращает False, чтобы не подавлять исключения.
        """

        return False

    # -- Descriptors

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Устанавливает имя дескриптора при определении класса.
        """

        self._descriptor_name = name

    def __get__(self, instance: Any, owner: type | None) -> Any:
        """
        Возвращает значение дескриптора для конкретного экземпляра.
        """

        if instance is None:
            return self

        return getattr(instance, f"_{self._descriptor_name}", None)

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Устанавливает значение дескриптора.
        """

        setattr(instance, f"_{self._descriptor_name}", value)

    def __delete__(self, instance: Any) -> None:
        """
        Удаляет значение дескриптора.
        """

        delattr(instance, f"_{self._descriptor_name}")

    # -- Class-related

    def __class__(self) -> type:
        """
        Возвращает класс экземпляра.
        """

        return type(self)

    def __instancecheck__(self, instance: object) -> bool:
        """
        Проверяет, является ли объект экземпляром этого класса.
        """

        return isinstance(instance, type(self))

    def __subclasscheck__(self, subclass: object) -> bool:
        """
        Проверяет, является ли класс подклассом этого класса.
        """

        return isinstance(subclass, type) and issubclass(subclass, type(self))

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Вызывается при создании подкласса.
        """

        super().__init_subclass__(**kwargs)

    # -- Hashing

    def __hash__(self) -> int:
        """
        Возвращает хеш для использования в set и dict.
        """

        return hash((self.name, self.age, self.value))

    # -- Pickle / serialization

    def __reduce__(self) -> tuple[object, tuple[Any, ...]]:
        """
        Поддержка pickle: возвращает информацию для восстановления объекта.
        """

        return (self.__class__, (self.name, self.age, self.value))

    def __reduce_ex__(self, protocol: int) -> tuple[Any, ...]:
        """
        Поддержка pickle для заданного протокола.
        """

        return self.__reduce__()

    def __getstate__(self) -> dict[str, Any]:
        """
        Возвращает состояние объекта для сериализации.
        """

        return dict(self.__dict__)

    def __setstate__(self, state: dict[str, Any]) -> None:
        """
        Восстанавливает состояние объекта из сериализованного словаря.
        """

        self.__dict__.update(state)

    # -- Generic typing

    def __class_getitem__(cls, item: Any) -> type:
        """
        Поддержка generic-синтаксиса класса: CExample[...].
        """

        return cls

    # -- Метаклассы

    def __prepare__(
        cls, name: str, bases: tuple[type, ...], **kwargs: Any
    ) -> dict[str, Any]:
        """
        Подготавливает пространство имён для создания класса.
        """

        return {}

    # Основные
    # __new__
    # __init__
    # __repr__
    # __str__
    # __len__
    # __iter__
    # __next__
    # __getitem__
    # __setitem__
    # __call__
    # __enter__
    # __exit__
    # __eq__
    # __hash__
    # __add__
    # __getattr__
    # __setattr__

    # -- Внутренние методы

    # -- __post_init__ в dataclasses


obj = CExample("Alex", 12, -9)

# __str__
print(obj)
print(str(obj))

print()

# __repr__
print(repr(obj))

print()

# __format__
print(f"{obj:short}")
print(f"{obj:full}")
print(f"{obj:_}")

print()

# __bytes__
print(bytes(obj))

print(dir(obj))
