from django.core.management.base import BaseCommand
from trainer.models import Language, Snippet

LANGUAGES = [
    {'slug': 'python',     'name': 'Python',               'icon': '🐍'},
    {'slug': 'javascript', 'name': 'JavaScript / TypeScript','icon': '🟨'},
    {'slug': 'java',       'name': 'Java',                  'icon': '☕'},
    {'slug': 'cpp',        'name': 'C++',                   'icon': '⚙️'},
    {'slug': 'go',         'name': 'Go',                    'icon': '🐹'},
    {'slug': 'sql',        'name': 'SQL',                   'icon': '🗄️'},
    {'slug': 'css',        'name': 'CSS',                   'icon': '🎨'},
]

SNIPPETS = {
    'python': {
        'easy': [
            {
                'title': 'Fibonacci generator',
                'code': (
                    'def fibonacci(n):\n'
                    '    a, b = 0, 1\n'
                    '    for _ in range(n):\n'
                    '        yield a\n'
                    '        a, b = b, a + b\n'
                ),
            },
            {
                'title': 'List flattener',
                'code': (
                    'def flatten(lst):\n'
                    '    result = []\n'
                    '    for item in lst:\n'
                    '        if isinstance(item, list):\n'
                    '            result.extend(flatten(item))\n'
                    '        else:\n'
                    '            result.append(item)\n'
                    '    return result\n'
                ),
            },
            {
                'title': 'Count words',
                'code': (
                    'def count_words(text):\n'
                    '    words = text.lower().split()\n'
                    '    counts = {}\n'
                    '    for word in words:\n'
                    '        counts[word] = counts.get(word, 0) + 1\n'
                    '    return counts\n'
                ),
            },
            {
                'title': 'Is palindrome',
                'code': (
                    'def is_palindrome(s):\n'
                    '    s = s.lower().replace(" ", "")\n'
                    '    return s == s[::-1]\n'
                    '\n'
                    '\n'
                    'assert is_palindrome("racecar")\n'
                    'assert not is_palindrome("hello")\n'
                ),
            },
            {
                'title': 'Temperature converter',
                'code': (
                    'def celsius_to_fahrenheit(c):\n'
                    '    return c * 9 / 5 + 32\n'
                    '\n'
                    'def fahrenheit_to_celsius(f):\n'
                    '    return (f - 32) * 5 / 9\n'
                    '\n'
                    'print(celsius_to_fahrenheit(100))\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Binary search',
                'code': (
                    'def binary_search(arr, target):\n'
                    '    lo, hi = 0, len(arr) - 1\n'
                    '    while lo <= hi:\n'
                    '        mid = (lo + hi) // 2\n'
                    '        if arr[mid] == target:\n'
                    '            return mid\n'
                    '        elif arr[mid] < target:\n'
                    '            lo = mid + 1\n'
                    '        else:\n'
                    '            hi = mid - 1\n'
                    '    return -1\n'
                ),
            },
            {
                'title': 'LRU Cache class',
                'code': (
                    'from collections import OrderedDict\n'
                    '\n'
                    'class LRUCache:\n'
                    '    def __init__(self, capacity):\n'
                    '        self.cache = OrderedDict()\n'
                    '        self.capacity = capacity\n'
                    '\n'
                    '    def get(self, key):\n'
                    '        if key not in self.cache:\n'
                    '            return -1\n'
                    '        self.cache.move_to_end(key)\n'
                    '        return self.cache[key]\n'
                ),
            },
            {
                'title': 'Merge sort',
                'code': (
                    'def merge_sort(arr):\n'
                    '    if len(arr) <= 1:\n'
                    '        return arr\n'
                    '    mid = len(arr) // 2\n'
                    '    left = merge_sort(arr[:mid])\n'
                    '    right = merge_sort(arr[mid:])\n'
                    '    return merge(left, right)\n'
                    '\n'
                    'def merge(left, right):\n'
                    '    result = []\n'
                    '    i = j = 0\n'
                ),
            },
            {
                'title': 'Dataclass with validator',
                'code': (
                    'from dataclasses import dataclass, field\n'
                    '\n'
                    '@dataclass\n'
                    'class Point:\n'
                    '    x: float\n'
                    '    y: float\n'
                    '    label: str = ""\n'
                    '\n'
                    '    def distance_to(self, other: "Point") -> float:\n'
                    '        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5\n'
                ),
            },
            {
                'title': 'Context manager',
                'code': (
                    'class Timer:\n'
                    '    def __init__(self, name=""):\n'
                    '        self.name = name\n'
                    '        self.elapsed = 0.0\n'
                    '\n'
                    '    def __enter__(self):\n'
                    '        import time\n'
                    '        self._start = time.perf_counter()\n'
                    '        return self\n'
                    '\n'
                    '    def __exit__(self, *args):\n'
                    '        import time\n'
                    '        self.elapsed = time.perf_counter() - self._start\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Decorator with arguments',
                'code': (
                    'import functools\n'
                    'import time\n'
                    '\n'
                    'def retry(times=3, delay=1.0, exceptions=(Exception,)):\n'
                    '    def decorator(func):\n'
                    '        @functools.wraps(func)\n'
                    '        def wrapper(*args, **kwargs):\n'
                    '            for attempt in range(times):\n'
                    '                try:\n'
                    '                    return func(*args, **kwargs)\n'
                    '                except exceptions as e:\n'
                    '                    if attempt == times - 1:\n'
                    '                        raise\n'
                    '                    time.sleep(delay)\n'
                    '        return wrapper\n'
                    '    return decorator\n'
                ),
            },
            {
                'title': 'Generic typed stack',
                'code': (
                    'from typing import Generic, TypeVar, Optional\n'
                    '\n'
                    'T = TypeVar("T")\n'
                    '\n'
                    'class Stack(Generic[T]):\n'
                    '    def __init__(self) -> None:\n'
                    '        self._items: list[T] = []\n'
                    '\n'
                    '    def push(self, item: T) -> None:\n'
                    '        self._items.append(item)\n'
                    '\n'
                    '    def pop(self) -> Optional[T]:\n'
                    '        return self._items.pop() if self._items else None\n'
                ),
            },
            {
                'title': 'Async HTTP fetch',
                'code': (
                    'import asyncio\n'
                    'import aiohttp\n'
                    '\n'
                    'async def fetch_all(urls: list[str]) -> list[dict]:\n'
                    '    async with aiohttp.ClientSession() as session:\n'
                    '        tasks = [fetch(session, url) for url in urls]\n'
                    '        return await asyncio.gather(*tasks)\n'
                    '\n'
                    'async def fetch(session, url: str) -> dict:\n'
                    '    async with session.get(url) as response:\n'
                    '        return await response.json()\n'
                ),
            },
            {
                'title': 'Metaclass singleton',
                'code': (
                    'class SingletonMeta(type):\n'
                    '    _instances: dict = {}\n'
                    '\n'
                    '    def __call__(cls, *args, **kwargs):\n'
                    '        if cls not in cls._instances:\n'
                    '            instance = super().__call__(*args, **kwargs)\n'
                    '            cls._instances[cls] = instance\n'
                    '        return cls._instances[cls]\n'
                    '\n'
                    'class Config(metaclass=SingletonMeta):\n'
                    '    def __init__(self):\n'
                    '        self.debug = False\n'
                ),
            },
            {
                'title': 'Protocol and structural subtyping',
                'code': (
                    'from typing import Protocol, runtime_checkable\n'
                    '\n'
                    '@runtime_checkable\n'
                    'class Drawable(Protocol):\n'
                    '    def draw(self) -> None: ...\n'
                    '    def resize(self, factor: float) -> None: ...\n'
                    '\n'
                    'class Circle:\n'
                    '    def draw(self) -> None:\n'
                    '        print("Drawing circle")\n'
                    '\n'
                    '    def resize(self, factor: float) -> None:\n'
                    '        self.radius *= factor\n'
                ),
            },
        ],
    },
    'javascript': {
        'easy': [
            {
                'title': 'Debounce function',
                'code': (
                    'function debounce(fn, delay) {\n'
                    '  let timer;\n'
                    '  return function (...args) {\n'
                    '    clearTimeout(timer);\n'
                    '    timer = setTimeout(() => fn.apply(this, args), delay);\n'
                    '  };\n'
                    '}\n'
                ),
            },
            {
                'title': 'Deep clone object',
                'code': (
                    'function deepClone(obj) {\n'
                    '  if (obj === null || typeof obj !== "object") return obj;\n'
                    '  if (Array.isArray(obj)) return obj.map(deepClone);\n'
                    '  return Object.fromEntries(\n'
                    '    Object.entries(obj).map(([k, v]) => [k, deepClone(v)])\n'
                    '  );\n'
                    '}\n'
                ),
            },
            {
                'title': 'Flatten array',
                'code': (
                    'function flattenDeep(arr) {\n'
                    '  return arr.reduce((acc, val) =>\n'
                    '    Array.isArray(val)\n'
                    '      ? acc.concat(flattenDeep(val))\n'
                    '      : acc.concat(val),\n'
                    '    []\n'
                    '  );\n'
                    '}\n'
                ),
            },
            {
                'title': 'Group by key',
                'code': (
                    'function groupBy(arr, key) {\n'
                    '  return arr.reduce((groups, item) => {\n'
                    '    const val = item[key];\n'
                    '    groups[val] = groups[val] || [];\n'
                    '    groups[val].push(item);\n'
                    '    return groups;\n'
                    '  }, {});\n'
                    '}\n'
                ),
            },
            {
                'title': 'Promise.all polyfill',
                'code': (
                    'function promiseAll(promises) {\n'
                    '  return new Promise((resolve, reject) => {\n'
                    '    const results = [];\n'
                    '    let remaining = promises.length;\n'
                    '    if (remaining === 0) { resolve(results); return; }\n'
                    '    promises.forEach((p, i) => {\n'
                    '      Promise.resolve(p).then(val => {\n'
                    '        results[i] = val;\n'
                    '        if (--remaining === 0) resolve(results);\n'
                    '      }).catch(reject);\n'
                    '    });\n'
                    '  });\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'EventEmitter class',
                'code': (
                    'class EventEmitter {\n'
                    '  constructor() {\n'
                    '    this.events = {};\n'
                    '  }\n'
                    '  on(event, listener) {\n'
                    '    (this.events[event] ||= []).push(listener);\n'
                    '    return this;\n'
                    '  }\n'
                    '  emit(event, ...args) {\n'
                    '    (this.events[event] || []).forEach(l => l(...args));\n'
                    '  }\n'
                    '  off(event, listener) {\n'
                    '    this.events[event] = (this.events[event] || []).filter(l => l !== listener);\n'
                    '  }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Memoize decorator',
                'code': (
                    'function memoize(fn) {\n'
                    '  const cache = new Map();\n'
                    '  return function (...args) {\n'
                    '    const key = JSON.stringify(args);\n'
                    '    if (cache.has(key)) return cache.get(key);\n'
                    '    const result = fn.apply(this, args);\n'
                    '    cache.set(key, result);\n'
                    '    return result;\n'
                    '  };\n'
                    '}\n'
                ),
            },
            {
                'title': 'TypeScript interface with generic',
                'code': (
                    'interface Repository<T extends { id: number }> {\n'
                    '  findById(id: number): Promise<T | null>;\n'
                    '  findAll(): Promise<T[]>;\n'
                    '  save(entity: Omit<T, "id">): Promise<T>;\n'
                    '  delete(id: number): Promise<void>;\n'
                    '}\n'
                    '\n'
                    'interface User {\n'
                    '  id: number;\n'
                    '  name: string;\n'
                    '  email: string;\n'
                    '}\n'
                ),
            },
            {
                'title': 'Async queue',
                'code': (
                    'class AsyncQueue {\n'
                    '  #queue = [];\n'
                    '  #running = 0;\n'
                    '  #concurrency;\n'
                    '  constructor(concurrency = 1) {\n'
                    '    this.#concurrency = concurrency;\n'
                    '  }\n'
                    '  enqueue(task) {\n'
                    '    return new Promise((resolve, reject) => {\n'
                    '      this.#queue.push({ task, resolve, reject });\n'
                    '      this.#run();\n'
                    '    });\n'
                    '  }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Observable pattern',
                'code': (
                    'class Observable {\n'
                    '  constructor(subscriber) {\n'
                    '    this._subscriber = subscriber;\n'
                    '  }\n'
                    '  subscribe(observer) {\n'
                    '    return this._subscriber(observer);\n'
                    '  }\n'
                    '  static from(iterable) {\n'
                    '    return new Observable(observer => {\n'
                    '      for (const item of iterable) observer.next(item);\n'
                    '      observer.complete();\n'
                    '    });\n'
                    '  }\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Proxy-based reactivity',
                'code': (
                    'function reactive(target, onChange) {\n'
                    '  return new Proxy(target, {\n'
                    '    set(obj, prop, value) {\n'
                    '      const old = obj[prop];\n'
                    '      obj[prop] = value;\n'
                    '      if (old !== value) onChange(prop, value, old);\n'
                    '      return true;\n'
                    '    },\n'
                    '    get(obj, prop) {\n'
                    '      const val = obj[prop];\n'
                    '      if (typeof val === "object" && val !== null)\n'
                    '        return reactive(val, onChange);\n'
                    '      return val;\n'
                    '    },\n'
                    '  });\n'
                    '}\n'
                ),
            },
            {
                'title': 'Typed state machine',
                'code': (
                    'type State = "idle" | "loading" | "success" | "error";\n'
                    'type Event = { type: "FETCH" } | { type: "RESOLVE"; data: unknown } | { type: "REJECT"; error: Error };\n'
                    '\n'
                    'function transition(state: State, event: Event): State {\n'
                    '  switch (state) {\n'
                    '    case "idle": return event.type === "FETCH" ? "loading" : state;\n'
                    '    case "loading":\n'
                    '      if (event.type === "RESOLVE") return "success";\n'
                    '      if (event.type === "REJECT") return "error";\n'
                    '      return state;\n'
                    '    default: return "idle";\n'
                    '  }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Middleware pipeline',
                'code': (
                    'type Middleware<T> = (ctx: T, next: () => Promise<void>) => Promise<void>;\n'
                    '\n'
                    'function compose<T>(middlewares: Middleware<T>[]) {\n'
                    '  return async (ctx: T) => {\n'
                    '    let index = -1;\n'
                    '    async function dispatch(i: number): Promise<void> {\n'
                    '      if (i <= index) throw new Error("next() called multiple times");\n'
                    '      index = i;\n'
                    '      const fn = middlewares[i];\n'
                    '      if (!fn) return;\n'
                    '      await fn(ctx, () => dispatch(i + 1));\n'
                    '    }\n'
                    '    return dispatch(0);\n'
                    '  };\n'
                    '}\n'
                ),
            },
            {
                'title': 'Decorator pattern TS',
                'code': (
                    'function log(target: any, key: string, descriptor: PropertyDescriptor) {\n'
                    '  const original = descriptor.value;\n'
                    '  descriptor.value = function (...args: unknown[]) {\n'
                    '    console.log(`Calling ${key} with`, args);\n'
                    '    const result = original.apply(this, args);\n'
                    '    console.log(`${key} returned`, result);\n'
                    '    return result;\n'
                    '  };\n'
                    '  return descriptor;\n'
                    '}\n'
                ),
            },
            {
                'title': 'Recursive type parser',
                'code': (
                    'type JSONValue =\n'
                    '  | string\n'
                    '  | number\n'
                    '  | boolean\n'
                    '  | null\n'
                    '  | JSONValue[]\n'
                    '  | { [key: string]: JSONValue };\n'
                    '\n'
                    'function parseJSON(input: string): JSONValue {\n'
                    '  return JSON.parse(input) as JSONValue;\n'
                    '}\n'
                    '\n'
                    'function serialize(val: JSONValue): string {\n'
                    '  return JSON.stringify(val, null, 2);\n'
                    '}\n'
                ),
            },
        ],
    },
    'java': {
        'easy': [
            {
                'title': 'Reverse string',
                'code': (
                    'public class StringUtils {\n'
                    '    public static String reverse(String s) {\n'
                    '        return new StringBuilder(s).reverse().toString();\n'
                    '    }\n'
                    '\n'
                    '    public static void main(String[] args) {\n'
                    '        System.out.println(reverse("hello"));\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Find max in array',
                'code': (
                    'public class ArrayUtils {\n'
                    '    public static int findMax(int[] arr) {\n'
                    '        int max = arr[0];\n'
                    '        for (int i = 1; i < arr.length; i++) {\n'
                    '            if (arr[i] > max) max = arr[i];\n'
                    '        }\n'
                    '        return max;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Factorial recursive',
                'code': (
                    'public class Math {\n'
                    '    public static long factorial(int n) {\n'
                    '        if (n < 0) throw new IllegalArgumentException();\n'
                    '        if (n == 0 || n == 1) return 1;\n'
                    '        return n * factorial(n - 1);\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Check prime',
                'code': (
                    'public class PrimeChecker {\n'
                    '    public static boolean isPrime(int n) {\n'
                    '        if (n < 2) return false;\n'
                    '        for (int i = 2; i <= Math.sqrt(n); i++) {\n'
                    '            if (n % i == 0) return false;\n'
                    '        }\n'
                    '        return true;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Stack with ArrayList',
                'code': (
                    'import java.util.ArrayList;\n'
                    '\n'
                    'public class Stack<T> {\n'
                    '    private ArrayList<T> list = new ArrayList<>();\n'
                    '\n'
                    '    public void push(T item) { list.add(item); }\n'
                    '    public T pop() { return list.remove(list.size() - 1); }\n'
                    '    public T peek() { return list.get(list.size() - 1); }\n'
                    '    public boolean isEmpty() { return list.isEmpty(); }\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Builder pattern',
                'code': (
                    'public class HttpRequest {\n'
                    '    private final String url;\n'
                    '    private final String method;\n'
                    '    private final String body;\n'
                    '\n'
                    '    private HttpRequest(Builder b) {\n'
                    '        this.url = b.url;\n'
                    '        this.method = b.method;\n'
                    '        this.body = b.body;\n'
                    '    }\n'
                    '\n'
                    '    public static class Builder {\n'
                    '        private String url, method = "GET", body;\n'
                    '        public Builder url(String u) { this.url = u; return this; }\n'
                    '        public Builder method(String m) { this.method = m; return this; }\n'
                    '        public Builder body(String b) { this.body = b; return this; }\n'
                    '        public HttpRequest build() { return new HttpRequest(this); }\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Generic Pair class',
                'code': (
                    'public class Pair<A, B> {\n'
                    '    private final A first;\n'
                    '    private final B second;\n'
                    '\n'
                    '    public Pair(A first, B second) {\n'
                    '        this.first = first;\n'
                    '        this.second = second;\n'
                    '    }\n'
                    '\n'
                    '    public A getFirst() { return first; }\n'
                    '    public B getSecond() { return second; }\n'
                    '\n'
                    '    public static <A, B> Pair<A, B> of(A a, B b) {\n'
                    '        return new Pair<>(a, b);\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Functional interface stream',
                'code': (
                    'import java.util.*;\n'
                    'import java.util.stream.*;\n'
                    '\n'
                    'public class StreamExample {\n'
                    '    public static Map<String, Long> countByCategory(List<String> items) {\n'
                    '        return items.stream()\n'
                    '            .collect(Collectors.groupingBy(\n'
                    '                s -> s.split(":")[0],\n'
                    '                Collectors.counting()\n'
                    '            ));\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Thread-safe counter',
                'code': (
                    'import java.util.concurrent.atomic.AtomicInteger;\n'
                    '\n'
                    'public class Counter {\n'
                    '    private final AtomicInteger count = new AtomicInteger(0);\n'
                    '\n'
                    '    public int increment() { return count.incrementAndGet(); }\n'
                    '    public int decrement() { return count.decrementAndGet(); }\n'
                    '    public int get() { return count.get(); }\n'
                    '    public void reset() { count.set(0); }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Optional chaining',
                'code': (
                    'import java.util.Optional;\n'
                    '\n'
                    'public class UserService {\n'
                    '    public Optional<String> getEmail(int userId) {\n'
                    '        return findUser(userId)\n'
                    '            .map(User::getProfile)\n'
                    '            .filter(Profile::isVerified)\n'
                    '            .map(Profile::getEmail);\n'
                    '    }\n'
                    '\n'
                    '    private Optional<User> findUser(int id) {\n'
                    '        return Optional.empty();\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'CompletableFuture chain',
                'code': (
                    'import java.util.concurrent.CompletableFuture;\n'
                    '\n'
                    'public class AsyncPipeline {\n'
                    '    public CompletableFuture<String> process(int id) {\n'
                    '        return CompletableFuture.supplyAsync(() -> fetchUser(id))\n'
                    '            .thenApplyAsync(user -> enrichUser(user))\n'
                    '            .thenApplyAsync(user -> serialize(user))\n'
                    '            .exceptionally(ex -> {\n'
                    '                System.err.println("Failed: " + ex.getMessage());\n'
                    '                return "{}";\n'
                    '            });\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Custom annotation processor',
                'code': (
                    'import java.lang.annotation.*;\n'
                    '\n'
                    '@Retention(RetentionPolicy.RUNTIME)\n'
                    '@Target(ElementType.METHOD)\n'
                    'public @interface Timed {\n'
                    '    String value() default "";\n'
                    '    TimeUnit unit() default TimeUnit.MILLISECONDS;\n'
                    '}\n'
                    '\n'
                    '@Timed(value = "fetchData", unit = TimeUnit.MICROSECONDS)\n'
                    'public void fetchData() {\n'
                    '    // measured method\n'
                    '}\n'
                ),
            },
            {
                'title': 'Sealed class hierarchy',
                'code': (
                    'public sealed interface Result<T>\n'
                    '    permits Result.Success, Result.Failure {\n'
                    '\n'
                    '    record Success<T>(T value) implements Result<T> {}\n'
                    '    record Failure<T>(String error) implements Result<T> {}\n'
                    '\n'
                    '    default <R> Result<R> map(java.util.function.Function<T, R> fn) {\n'
                    '        return switch (this) {\n'
                    '            case Success<T> s -> new Success<>(fn.apply(s.value()));\n'
                    '            case Failure<T> f -> new Failure<>(f.error());\n'
                    '        };\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Reactive publisher',
                'code': (
                    'import java.util.concurrent.Flow.*;\n'
                    '\n'
                    'public class RangePublisher implements Publisher<Integer> {\n'
                    '    private final int start, end;\n'
                    '    public RangePublisher(int start, int end) {\n'
                    '        this.start = start; this.end = end;\n'
                    '    }\n'
                    '    @Override\n'
                    '    public void subscribe(Subscriber<? super Integer> subscriber) {\n'
                    '        subscriber.onSubscribe(new RangeSubscription(subscriber, start, end));\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Lock-free stack',
                'code': (
                    'import java.util.concurrent.atomic.AtomicReference;\n'
                    '\n'
                    'public class LockFreeStack<T> {\n'
                    '    private record Node<T>(T value, Node<T> next) {}\n'
                    '    private final AtomicReference<Node<T>> top = new AtomicReference<>();\n'
                    '\n'
                    '    public void push(T val) {\n'
                    '        Node<T> newNode;\n'
                    '        do { newNode = new Node<>(val, top.get());\n'
                    '        } while (!top.compareAndSet(newNode.next(), newNode));\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
    },
    'cpp': {
        'easy': [
            {
                'title': 'Bubble sort',
                'code': (
                    '#include <vector>\n'
                    '#include <utility>\n'
                    '\n'
                    'void bubbleSort(std::vector<int>& arr) {\n'
                    '    for (size_t i = 0; i < arr.size(); ++i)\n'
                    '        for (size_t j = 0; j < arr.size() - i - 1; ++j)\n'
                    '            if (arr[j] > arr[j + 1])\n'
                    '                std::swap(arr[j], arr[j + 1]);\n'
                    '}\n'
                ),
            },
            {
                'title': 'String split function',
                'code': (
                    '#include <string>\n'
                    '#include <vector>\n'
                    '#include <sstream>\n'
                    '\n'
                    'std::vector<std::string> split(const std::string& s, char delim) {\n'
                    '    std::vector<std::string> tokens;\n'
                    '    std::istringstream ss(s);\n'
                    '    std::string token;\n'
                    '    while (std::getline(ss, token, delim)) tokens.push_back(token);\n'
                    '    return tokens;\n'
                    '}\n'
                ),
            },
            {
                'title': 'Stack with template',
                'code': (
                    '#include <vector>\n'
                    '#include <stdexcept>\n'
                    '\n'
                    'template<typename T>\n'
                    'class Stack {\n'
                    '    std::vector<T> data;\n'
                    'public:\n'
                    '    void push(T val) { data.push_back(val); }\n'
                    '    T pop() {\n'
                    '        if (data.empty()) throw std::underflow_error("empty");\n'
                    '        T top = data.back(); data.pop_back(); return top;\n'
                    '    }\n'
                    '    bool empty() const { return data.empty(); }\n'
                    '};\n'
                ),
            },
            {
                'title': 'GCD with Euclid',
                'code': (
                    '#include <iostream>\n'
                    '\n'
                    'int gcd(int a, int b) {\n'
                    '    while (b != 0) {\n'
                    '        int t = b;\n'
                    '        b = a % b;\n'
                    '        a = t;\n'
                    '    }\n'
                    '    return a;\n'
                    '}\n'
                    '\n'
                    'int lcm(int a, int b) { return a / gcd(a, b) * b; }\n'
                ),
            },
            {
                'title': 'Linked list node',
                'code': (
                    'template<typename T>\n'
                    'struct Node {\n'
                    '    T data;\n'
                    '    Node* next;\n'
                    '    explicit Node(T val) : data(val), next(nullptr) {}\n'
                    '};\n'
                    '\n'
                    'template<typename T>\n'
                    'void append(Node<T>*& head, T val) {\n'
                    '    Node<T>* node = new Node<T>(val);\n'
                    '    if (!head) { head = node; return; }\n'
                    '    Node<T>* cur = head;\n'
                    '    while (cur->next) cur = cur->next;\n'
                    '    cur->next = node;\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'RAII file wrapper',
                'code': (
                    '#include <fstream>\n'
                    '#include <string>\n'
                    '#include <stdexcept>\n'
                    '\n'
                    'class FileReader {\n'
                    '    std::ifstream file;\n'
                    'public:\n'
                    '    explicit FileReader(const std::string& path) : file(path) {\n'
                    '        if (!file.is_open()) throw std::runtime_error("Cannot open: " + path);\n'
                    '    }\n'
                    '    std::string readAll() {\n'
                    '        return std::string(std::istreambuf_iterator<char>(file), {});\n'
                    '    }\n'
                    '    ~FileReader() { if (file.is_open()) file.close(); }\n'
                    '};\n'
                ),
            },
            {
                'title': 'Variadic template sum',
                'code': (
                    '#include <concepts>\n'
                    '\n'
                    'template<typename T>\n'
                    'concept Numeric = std::integral<T> || std::floating_point<T>;\n'
                    '\n'
                    'template<Numeric... Args>\n'
                    'auto sum(Args... args) {\n'
                    '    return (args + ...);\n'
                    '}\n'
                    '\n'
                    'auto total = sum(1, 2.5, 3L, 4.0f);\n'
                ),
            },
            {
                'title': 'Move semantics example',
                'code': (
                    '#include <string>\n'
                    '#include <utility>\n'
                    '\n'
                    'class Buffer {\n'
                    '    std::string data;\n'
                    'public:\n'
                    '    explicit Buffer(std::string d) : data(std::move(d)) {}\n'
                    '    Buffer(Buffer&& other) noexcept : data(std::move(other.data)) {}\n'
                    '    Buffer& operator=(Buffer&& other) noexcept {\n'
                    '        if (this != &other) data = std::move(other.data);\n'
                    '        return *this;\n'
                    '    }\n'
                    '    const std::string& get() const { return data; }\n'
                    '};\n'
                ),
            },
            {
                'title': 'Custom iterator',
                'code': (
                    '#include <iterator>\n'
                    '\n'
                    'class Range {\n'
                    '    int start_, end_;\n'
                    'public:\n'
                    '    Range(int s, int e) : start_(s), end_(e) {}\n'
                    '    struct Iterator {\n'
                    '        int cur;\n'
                    '        Iterator(int c) : cur(c) {}\n'
                    '        int operator*() const { return cur; }\n'
                    '        Iterator& operator++() { ++cur; return *this; }\n'
                    '        bool operator!=(const Iterator& o) const { return cur != o.cur; }\n'
                    '    };\n'
                    '    Iterator begin() { return {start_}; }\n'
                    '    Iterator end()   { return {end_}; }\n'
                    '};\n'
                ),
            },
            {
                'title': 'Lambda with capture',
                'code': (
                    '#include <algorithm>\n'
                    '#include <vector>\n'
                    '\n'
                    'std::vector<int> filterAndTransform(\n'
                    '    const std::vector<int>& src, int threshold) {\n'
                    '    std::vector<int> result;\n'
                    '    std::copy_if(src.begin(), src.end(),\n'
                    '        std::back_inserter(result),\n'
                    '        [threshold](int x) { return x > threshold; });\n'
                    '    std::transform(result.begin(), result.end(),\n'
                    '        result.begin(), [](int x) { return x * x; });\n'
                    '    return result;\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Coroutine generator C++20',
                'code': (
                    '#include <coroutine>\n'
                    '#include <optional>\n'
                    '\n'
                    'template<typename T>\n'
                    'struct Generator {\n'
                    '    struct promise_type {\n'
                    '        T value;\n'
                    '        std::suspend_always yield_value(T v) { value = v; return {}; }\n'
                    '        std::suspend_always initial_suspend() { return {}; }\n'
                    '        std::suspend_always final_suspend() noexcept { return {}; }\n'
                    '        Generator get_return_object() { return Generator{this}; }\n'
                    '        void return_void() {}\n'
                    '        void unhandled_exception() { std::terminate(); }\n'
                    '    };\n'
                    '    using handle_t = std::coroutine_handle<promise_type>;\n'
                    '    handle_t handle;\n'
                    '    explicit Generator(promise_type* p) : handle(handle_t::from_promise(*p)) {}\n'
                    '    ~Generator() { if (handle) handle.destroy(); }\n'
                    '};\n'
                ),
            },
            {
                'title': 'SFINAE enable_if',
                'code': (
                    '#include <type_traits>\n'
                    '#include <string>\n'
                    '\n'
                    'template<typename T,\n'
                    '    typename = std::enable_if_t<std::is_arithmetic_v<T>>>\n'
                    'T clamp(T val, T lo, T hi) {\n'
                    '    return val < lo ? lo : val > hi ? hi : val;\n'
                    '}\n'
                    '\n'
                    'template<typename T>\n'
                    'std::enable_if_t<std::is_convertible_v<T, std::string>, std::string>\n'
                    'toString(T&& val) { return std::string(std::forward<T>(val)); }\n'
                ),
            },
            {
                'title': 'Lock-free spinlock',
                'code': (
                    '#include <atomic>\n'
                    '\n'
                    'class Spinlock {\n'
                    '    std::atomic_flag flag = ATOMIC_FLAG_INIT;\n'
                    'public:\n'
                    '    void lock() noexcept {\n'
                    '        while (flag.test_and_set(std::memory_order_acquire))\n'
                    '            flag.wait(true, std::memory_order_relaxed);\n'
                    '    }\n'
                    '    void unlock() noexcept {\n'
                    '        flag.clear(std::memory_order_release);\n'
                    '        flag.notify_one();\n'
                    '    }\n'
                    '};\n'
                ),
            },
            {
                'title': 'Policy-based design',
                'code': (
                    'template<typename StoragePolicy, typename LoggingPolicy>\n'
                    'class DataProcessor : public StoragePolicy, public LoggingPolicy {\n'
                    'public:\n'
                    '    void process(const std::string& data) {\n'
                    '        LoggingPolicy::log("Processing: " + data);\n'
                    '        StoragePolicy::store(data);\n'
                    '    }\n'
                    '};\n'
                    '\n'
                    'struct ConsoleLogger { void log(const std::string& m) { std::cout << m; } };\n'
                    'struct MemoryStore { void store(const std::string& d) { buffer.push_back(d); }\n'
                    '    std::vector<std::string> buffer; };\n'
                ),
            },
            {
                'title': 'Type-erased function',
                'code': (
                    '#include <memory>\n'
                    '#include <functional>\n'
                    '\n'
                    'template<typename Sig> class Function;\n'
                    '\n'
                    'template<typename R, typename... Args>\n'
                    'class Function<R(Args...)> {\n'
                    '    struct Base { virtual R call(Args...) = 0; virtual ~Base() = default; };\n'
                    '    template<typename F>\n'
                    '    struct Impl : Base {\n'
                    '        F fn;\n'
                    '        Impl(F f) : fn(std::move(f)) {}\n'
                    '        R call(Args... args) override { return fn(args...); }\n'
                    '    };\n'
                    '    std::unique_ptr<Base> ptr;\n'
                    'public:\n'
                    '    template<typename F> Function(F f) : ptr(std::make_unique<Impl<F>>(std::move(f))) {}\n'
                    '    R operator()(Args... args) { return ptr->call(args...); }\n'
                    '};\n'
                ),
            },
        ],
    },
    'go': {
        'easy': [
            {
                'title': 'Map word frequency',
                'code': (
                    'package main\n'
                    '\n'
                    'import "strings"\n'
                    '\n'
                    'func wordFreq(s string) map[string]int {\n'
                    '    counts := make(map[string]int)\n'
                    '    for _, word := range strings.Fields(s) {\n'
                    '        counts[strings.ToLower(word)]++\n'
                    '    }\n'
                    '    return counts\n'
                    '}\n'
                ),
            },
            {
                'title': 'Fibonacci channel',
                'code': (
                    'package main\n'
                    '\n'
                    'func fibonacci(n int, ch chan<- int) {\n'
                    '    a, b := 0, 1\n'
                    '    for i := 0; i < n; i++ {\n'
                    '        ch <- a\n'
                    '        a, b = b, a+b\n'
                    '    }\n'
                    '    close(ch)\n'
                    '}\n'
                ),
            },
            {
                'title': 'Error wrapping',
                'code': (
                    'package main\n'
                    '\n'
                    'import (\n'
                    '    "errors"\n'
                    '    "fmt"\n'
                    ')\n'
                    '\n'
                    'var ErrNotFound = errors.New("not found")\n'
                    '\n'
                    'func findUser(id int) error {\n'
                    '    return fmt.Errorf("findUser %d: %w", id, ErrNotFound)\n'
                    '}\n'
                ),
            },
            {
                'title': 'Closure counter',
                'code': (
                    'package main\n'
                    '\n'
                    'func makeCounter(start int) func() int {\n'
                    '    n := start\n'
                    '    return func() int {\n'
                    '        n++\n'
                    '        return n\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Struct with method',
                'code': (
                    'package main\n'
                    '\n'
                    'type Rectangle struct {\n'
                    '    Width, Height float64\n'
                    '}\n'
                    '\n'
                    'func (r Rectangle) Area() float64 {\n'
                    '    return r.Width * r.Height\n'
                    '}\n'
                    '\n'
                    'func (r Rectangle) Perimeter() float64 {\n'
                    '    return 2 * (r.Width + r.Height)\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Generic map function',
                'code': (
                    'package main\n'
                    '\n'
                    'func Map[T, U any](s []T, f func(T) U) []U {\n'
                    '    result := make([]U, len(s))\n'
                    '    for i, v := range s {\n'
                    '        result[i] = f(v)\n'
                    '    }\n'
                    '    return result\n'
                    '}\n'
                    '\n'
                    'func Filter[T any](s []T, pred func(T) bool) []T {\n'
                    '    var result []T\n'
                    '    for _, v := range s {\n'
                    '        if pred(v) { result = append(result, v) }\n'
                    '    }\n'
                    '    return result\n'
                    '}\n'
                ),
            },
            {
                'title': 'Goroutine fan-out',
                'code': (
                    'package main\n'
                    '\n'
                    'import "sync"\n'
                    '\n'
                    'func fanOut(in <-chan int, workers int) []<-chan int {\n'
                    '    outs := make([]<-chan int, workers)\n'
                    '    for i := range outs {\n'
                    '        ch := make(chan int)\n'
                    '        outs[i] = ch\n'
                    '        go func(out chan<- int) {\n'
                    '            defer close(out)\n'
                    '            for v := range in { out <- v }\n'
                    '        }(ch)\n'
                    '    }\n'
                    '    return outs\n'
                    '}\n'
                ),
            },
            {
                'title': 'Interface Stringer',
                'code': (
                    'package main\n'
                    '\n'
                    'import "fmt"\n'
                    '\n'
                    'type Color int\n'
                    '\n'
                    'const (\n'
                    '    Red Color = iota\n'
                    '    Green\n'
                    '    Blue\n'
                    ')\n'
                    '\n'
                    'func (c Color) String() string {\n'
                    '    return [...]string{"Red", "Green", "Blue"}[c]\n'
                    '}\n'
                    '\n'
                    'func main() { fmt.Println(Green) }\n'
                ),
            },
            {
                'title': 'HTTP middleware',
                'code': (
                    'package main\n'
                    '\n'
                    'import (\n'
                    '    "log"\n'
                    '    "net/http"\n'
                    '    "time"\n'
                    ')\n'
                    '\n'
                    'func logging(next http.Handler) http.Handler {\n'
                    '    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {\n'
                    '        start := time.Now()\n'
                    '        next.ServeHTTP(w, r)\n'
                    '        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))\n'
                    '    })\n'
                    '}\n'
                ),
            },
            {
                'title': 'Context with cancel',
                'code': (
                    'package main\n'
                    '\n'
                    'import (\n'
                    '    "context"\n'
                    '    "time"\n'
                    ')\n'
                    '\n'
                    'func doWork(ctx context.Context) error {\n'
                    '    for {\n'
                    '        select {\n'
                    '        case <-ctx.Done():\n'
                    '            return ctx.Err()\n'
                    '        case <-time.After(100 * time.Millisecond):\n'
                    '            // simulate work\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Worker pool',
                'code': (
                    'package main\n'
                    '\n'
                    'import "sync"\n'
                    '\n'
                    'type WorkerPool struct {\n'
                    '    tasks   chan func()\n'
                    '    wg      sync.WaitGroup\n'
                    '}\n'
                    '\n'
                    'func NewWorkerPool(size int) *WorkerPool {\n'
                    '    p := &WorkerPool{tasks: make(chan func(), 100)}\n'
                    '    for i := 0; i < size; i++ {\n'
                    '        p.wg.Add(1)\n'
                    '        go func() {\n'
                    '            defer p.wg.Done()\n'
                    '            for task := range p.tasks { task() }\n'
                    '        }()\n'
                    '    }\n'
                    '    return p\n'
                    '}\n'
                ),
            },
            {
                'title': 'Circuit breaker',
                'code': (
                    'package main\n'
                    '\n'
                    'import (\n'
                    '    "errors"\n'
                    '    "sync"\n'
                    '    "time"\n'
                    ')\n'
                    '\n'
                    'type CircuitBreaker struct {\n'
                    '    mu         sync.Mutex\n'
                    '    failures   int\n'
                    '    maxFails   int\n'
                    '    resetAfter time.Duration\n'
                    '    openUntil  time.Time\n'
                    '}\n'
                    '\n'
                    'var ErrOpen = errors.New("circuit breaker is open")\n'
                ),
            },
            {
                'title': 'Generic Result type',
                'code': (
                    'package main\n'
                    '\n'
                    'type Result[T any] struct {\n'
                    '    value T\n'
                    '    err   error\n'
                    '}\n'
                    '\n'
                    'func Ok[T any](v T) Result[T]       { return Result[T]{value: v} }\n'
                    'func Err[T any](e error) Result[T]  { return Result[T]{err: e} }\n'
                    '\n'
                    'func (r Result[T]) Unwrap() (T, error) { return r.value, r.err }\n'
                    '\n'
                    'func Map[T, U any](r Result[T], f func(T) U) Result[U] {\n'
                    '    if r.err != nil { return Err[U](r.err) }\n'
                    '    return Ok(f(r.value))\n'
                    '}\n'
                ),
            },
            {
                'title': 'Sieve of Eratosthenes channel',
                'code': (
                    'package main\n'
                    '\n'
                    'func generate(ch chan<- int) {\n'
                    '    for i := 2; ; i++ { ch <- i }\n'
                    '}\n'
                    '\n'
                    'func filter(in <-chan int, out chan<- int, prime int) {\n'
                    '    for v := range in {\n'
                    '        if v%prime != 0 { out <- v }\n'
                    '    }\n'
                    '}\n'
                    '\n'
                    'func primes(n int) []int {\n'
                    '    ch := make(chan int)\n'
                    '    go generate(ch)\n'
                    '    var result []int\n'
                    '    for i := 0; i < n; i++ {\n'
                    '        prime := <-ch\n'
                    '        result = append(result, prime)\n'
                    '        ch1 := make(chan int)\n'
                    '        go filter(ch, ch1, prime)\n'
                    '        ch = ch1\n'
                    '    }\n'
                    '    return result\n'
                    '}\n'
                ),
            },
            {
                'title': 'Trie data structure',
                'code': (
                    'package main\n'
                    '\n'
                    'type TrieNode struct {\n'
                    '    children [26]*TrieNode\n'
                    '    isEnd    bool\n'
                    '}\n'
                    '\n'
                    'type Trie struct{ root *TrieNode }\n'
                    '\n'
                    'func (t *Trie) Insert(word string) {\n'
                    '    cur := t.root\n'
                    '    for _, ch := range word {\n'
                    '        idx := ch - \'a\'\n'
                    '        if cur.children[idx] == nil {\n'
                    '            cur.children[idx] = &TrieNode{}\n'
                    '        }\n'
                    '        cur = cur.children[idx]\n'
                    '    }\n'
                    '    cur.isEnd = true\n'
                    '}\n'
                ),
            },
        ],
    },
    'sql': {
        'easy': [
            {
                'title': 'Create users table',
                'code': (
                    'CREATE TABLE users (\n'
                    '    id          SERIAL PRIMARY KEY,\n'
                    '    username    VARCHAR(50) NOT NULL UNIQUE,\n'
                    '    email       VARCHAR(255) NOT NULL UNIQUE,\n'
                    '    password    VARCHAR(255) NOT NULL,\n'
                    '    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n'
                    '    is_active   BOOLEAN DEFAULT TRUE\n'
                    ');\n'
                ),
            },
            {
                'title': 'Select with join',
                'code': (
                    'SELECT\n'
                    '    u.username,\n'
                    '    u.email,\n'
                    '    p.bio,\n'
                    '    p.avatar_url\n'
                    'FROM users u\n'
                    'INNER JOIN profiles p ON p.user_id = u.id\n'
                    'WHERE u.is_active = TRUE\n'
                    'ORDER BY u.created_at DESC\n'
                    'LIMIT 20;\n'
                ),
            },
            {
                'title': 'Aggregation query',
                'code': (
                    'SELECT\n'
                    '    category,\n'
                    '    COUNT(*) AS total,\n'
                    '    SUM(price) AS revenue,\n'
                    '    AVG(price) AS avg_price,\n'
                    '    MAX(price) AS max_price\n'
                    'FROM products\n'
                    'WHERE is_published = TRUE\n'
                    'GROUP BY category\n'
                    'HAVING COUNT(*) > 5\n'
                    'ORDER BY revenue DESC;\n'
                ),
            },
            {
                'title': 'Update with subquery',
                'code': (
                    'UPDATE orders\n'
                    'SET status = \'completed\',\n'
                    '    completed_at = NOW()\n'
                    'WHERE id IN (\n'
                    '    SELECT o.id\n'
                    '    FROM orders o\n'
                    '    JOIN payments p ON p.order_id = o.id\n'
                    '    WHERE p.status = \'paid\'\n'
                    '      AND o.status = \'pending\'\n'
                    ');\n'
                ),
            },
            {
                'title': 'Create index',
                'code': (
                    'CREATE INDEX CONCURRENTLY idx_orders_user_status\n'
                    '    ON orders (user_id, status)\n'
                    '    WHERE status != \'deleted\';\n'
                    '\n'
                    'CREATE UNIQUE INDEX idx_users_email\n'
                    '    ON users (LOWER(email));\n'
                    '\n'
                    'ANALYZE orders;\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Window function ranking',
                'code': (
                    'SELECT\n'
                    '    employee_id,\n'
                    '    department,\n'
                    '    salary,\n'
                    '    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,\n'
                    '    DENSE_RANK() OVER (ORDER BY salary DESC) AS overall_rank,\n'
                    '    LAG(salary) OVER (PARTITION BY department ORDER BY hire_date) AS prev_salary\n'
                    'FROM employees\n'
                    'WHERE is_active = TRUE;\n'
                ),
            },
            {
                'title': 'CTE recursive tree',
                'code': (
                    'WITH RECURSIVE category_tree AS (\n'
                    '    SELECT id, name, parent_id, 0 AS depth\n'
                    '    FROM categories\n'
                    '    WHERE parent_id IS NULL\n'
                    '    UNION ALL\n'
                    '    SELECT c.id, c.name, c.parent_id, ct.depth + 1\n'
                    '    FROM categories c\n'
                    '    JOIN category_tree ct ON ct.id = c.parent_id\n'
                    ')\n'
                    'SELECT * FROM category_tree ORDER BY depth, name;\n'
                ),
            },
            {
                'title': 'JSON aggregation',
                'code': (
                    'SELECT\n'
                    '    u.id,\n'
                    '    u.username,\n'
                    '    JSON_AGG(\n'
                    '        JSON_BUILD_OBJECT(\n'
                    '            \'id\', o.id,\n'
                    '            \'total\', o.total,\n'
                    '            \'status\', o.status\n'
                    '        ) ORDER BY o.created_at DESC\n'
                    '    ) FILTER (WHERE o.id IS NOT NULL) AS orders\n'
                    'FROM users u\n'
                    'LEFT JOIN orders o ON o.user_id = u.id\n'
                    'GROUP BY u.id, u.username;\n'
                ),
            },
            {
                'title': 'Upsert pattern',
                'code': (
                    'INSERT INTO product_stats (product_id, views, last_viewed)\n'
                    'VALUES ($1, 1, NOW())\n'
                    'ON CONFLICT (product_id) DO UPDATE\n'
                    '    SET views = product_stats.views + EXCLUDED.views,\n'
                    '        last_viewed = EXCLUDED.last_viewed\n'
                    'RETURNING product_id, views, last_viewed;\n'
                ),
            },
            {
                'title': 'Full-text search',
                'code': (
                    'SELECT\n'
                    '    id,\n'
                    '    title,\n'
                    '    ts_rank(search_vector, query) AS rank\n'
                    'FROM articles,\n'
                    '    to_tsquery(\'english\', $1) AS query\n'
                    'WHERE search_vector @@ query\n'
                    'ORDER BY rank DESC\n'
                    'LIMIT 20;\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Materialized view with refresh',
                'code': (
                    'CREATE MATERIALIZED VIEW monthly_revenue AS\n'
                    'SELECT\n'
                    '    DATE_TRUNC(\'month\', created_at) AS month,\n'
                    '    product_id,\n'
                    '    SUM(quantity * unit_price) AS revenue,\n'
                    '    COUNT(DISTINCT user_id) AS unique_buyers\n'
                    'FROM order_items oi\n'
                    'JOIN orders o ON o.id = oi.order_id\n'
                    'WHERE o.status = \'completed\'\n'
                    'GROUP BY 1, 2\n'
                    'WITH DATA;\n'
                    '\n'
                    'CREATE UNIQUE INDEX ON monthly_revenue (month, product_id);\n'
                    'REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue;\n'
                ),
            },
            {
                'title': 'Partition table by range',
                'code': (
                    'CREATE TABLE events (\n'
                    '    id          BIGSERIAL,\n'
                    '    user_id     BIGINT NOT NULL,\n'
                    '    event_type  VARCHAR(50) NOT NULL,\n'
                    '    payload     JSONB,\n'
                    '    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()\n'
                    ') PARTITION BY RANGE (created_at);\n'
                    '\n'
                    'CREATE TABLE events_2025\n'
                    '    PARTITION OF events\n'
                    '    FOR VALUES FROM (\'2025-01-01\') TO (\'2026-01-01\');\n'
                    '\n'
                    'CREATE INDEX ON events (user_id, created_at);\n'
                ),
            },
            {
                'title': 'Lateral join with limit',
                'code': (
                    'SELECT\n'
                    '    u.id,\n'
                    '    u.username,\n'
                    '    latest.title AS last_post_title,\n'
                    '    latest.created_at AS last_post_date\n'
                    'FROM users u\n'
                    'CROSS JOIN LATERAL (\n'
                    '    SELECT title, created_at\n'
                    '    FROM posts\n'
                    '    WHERE user_id = u.id\n'
                    '    ORDER BY created_at DESC\n'
                    '    LIMIT 1\n'
                    ') AS latest\n'
                    'WHERE u.is_active = TRUE;\n'
                ),
            },
            {
                'title': 'Trigger function',
                'code': (
                    'CREATE OR REPLACE FUNCTION update_timestamp()\n'
                    'RETURNS TRIGGER AS $$\n'
                    'BEGIN\n'
                    '    NEW.updated_at = NOW();\n'
                    '    NEW.version = OLD.version + 1;\n'
                    '    RETURN NEW;\n'
                    'END;\n'
                    '$$ LANGUAGE plpgsql;\n'
                    '\n'
                    'CREATE TRIGGER trg_update_timestamp\n'
                    'BEFORE UPDATE ON documents\n'
                    'FOR EACH ROW EXECUTE FUNCTION update_timestamp();\n'
                ),
            },
            {
                'title': 'Advisory lock pattern',
                'code': (
                    'DO $$\n'
                    'DECLARE\n'
                    '    lock_id BIGINT := 12345;\n'
                    'BEGIN\n'
                    '    IF pg_try_advisory_lock(lock_id) THEN\n'
                    '        BEGIN\n'
                    '            PERFORM process_pending_jobs();\n'
                    '        EXCEPTION WHEN OTHERS THEN\n'
                    '            PERFORM pg_advisory_unlock(lock_id);\n'
                    '            RAISE;\n'
                    '        END;\n'
                    '        PERFORM pg_advisory_unlock(lock_id);\n'
                    '    ELSE\n'
                    '        RAISE NOTICE \'Another process holds the lock\';\n'
                    '    END IF;\n'
                    'END;\n'
                    '$$;\n'
                ),
            },
        ],
    },
    'css': {
        'easy': [
            {
                'title': 'Flexbox center',
                'code': (
                    '.container {\n'
                    '    display: flex;\n'
                    '    align-items: center;\n'
                    '    justify-content: center;\n'
                    '    min-height: 100vh;\n'
                    '}\n'
                ),
            },
            {
                'title': 'CSS variables',
                'code': (
                    ':root {\n'
                    '    --primary: #6c63ff;\n'
                    '    --bg: #0f0f1a;\n'
                    '    --text: #e8eaf6;\n'
                    '    --radius: 8px;\n'
                    '    --shadow: 0 4px 16px rgba(0,0,0,.4);\n'
                    '}\n'
                ),
            },
            {
                'title': 'Button hover animation',
                'code': (
                    '.btn {\n'
                    '    background: var(--primary);\n'
                    '    color: #fff;\n'
                    '    padding: .6rem 1.4rem;\n'
                    '    border: none;\n'
                    '    border-radius: var(--radius);\n'
                    '    cursor: pointer;\n'
                    '    transition: transform .15s ease, box-shadow .15s ease;\n'
                    '}\n'
                    '.btn:hover {\n'
                    '    transform: translateY(-2px);\n'
                    '    box-shadow: 0 8px 20px rgba(108,99,255,.35);\n'
                    '}\n'
                ),
            },
            {
                'title': 'Media query breakpoint',
                'code': (
                    '.grid {\n'
                    '    display: grid;\n'
                    '    grid-template-columns: repeat(3, 1fr);\n'
                    '    gap: 1rem;\n'
                    '}\n'
                    '\n'
                    '@media (max-width: 768px) {\n'
                    '    .grid {\n'
                    '        grid-template-columns: 1fr;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Text gradient',
                'code': (
                    '.gradient-text {\n'
                    '    background: linear-gradient(135deg, #6c63ff, #e040fb);\n'
                    '    -webkit-background-clip: text;\n'
                    '    -webkit-text-fill-color: transparent;\n'
                    '    background-clip: text;\n'
                    '    font-weight: 800;\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Glassmorphism card',
                'code': (
                    '.glass-card {\n'
                    '    background: rgba(255, 255, 255, 0.06);\n'
                    '    backdrop-filter: blur(12px);\n'
                    '    -webkit-backdrop-filter: blur(12px);\n'
                    '    border: 1px solid rgba(255, 255, 255, 0.12);\n'
                    '    border-radius: 16px;\n'
                    '    padding: 2rem;\n'
                    '    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);\n'
                    '    transition: transform 0.2s ease, box-shadow 0.2s ease;\n'
                    '}\n'
                    '.glass-card:hover {\n'
                    '    transform: translateY(-4px);\n'
                    '    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);\n'
                    '}\n'
                ),
            },
            {
                'title': 'Custom checkbox',
                'code': (
                    '.checkbox-wrapper input[type="checkbox"] {\n'
                    '    display: none;\n'
                    '}\n'
                    '.checkbox-wrapper label {\n'
                    '    display: flex;\n'
                    '    align-items: center;\n'
                    '    gap: .6rem;\n'
                    '    cursor: pointer;\n'
                    '}\n'
                    '.checkbox-wrapper label::before {\n'
                    '    content: "";\n'
                    '    width: 18px;\n'
                    '    height: 18px;\n'
                    '    border: 2px solid #6c63ff;\n'
                    '    border-radius: 4px;\n'
                    '    transition: background .15s;\n'
                    '}\n'
                    '.checkbox-wrapper input:checked + label::before {\n'
                    '    background: #6c63ff;\n'
                    '}\n'
                ),
            },
            {
                'title': 'CSS-only tooltip',
                'code': (
                    '.tooltip {\n'
                    '    position: relative;\n'
                    '    display: inline-block;\n'
                    '}\n'
                    '.tooltip::after {\n'
                    '    content: attr(data-tip);\n'
                    '    position: absolute;\n'
                    '    bottom: calc(100% + 8px);\n'
                    '    left: 50%;\n'
                    '    transform: translateX(-50%);\n'
                    '    background: #1a1a2e;\n'
                    '    color: #e8eaf6;\n'
                    '    padding: .35rem .7rem;\n'
                    '    border-radius: 6px;\n'
                    '    font-size: .78rem;\n'
                    '    white-space: nowrap;\n'
                    '    opacity: 0;\n'
                    '    pointer-events: none;\n'
                    '    transition: opacity .15s ease;\n'
                    '}\n'
                    '.tooltip:hover::after { opacity: 1; }\n'
                ),
            },
            {
                'title': 'Sticky navbar with blur',
                'code': (
                    '.navbar {\n'
                    '    position: sticky;\n'
                    '    top: 0;\n'
                    '    z-index: 100;\n'
                    '    background: rgba(13, 15, 23, 0.8);\n'
                    '    backdrop-filter: blur(16px);\n'
                    '    -webkit-backdrop-filter: blur(16px);\n'
                    '    border-bottom: 1px solid rgba(255, 255, 255, 0.07);\n'
                    '    display: flex;\n'
                    '    align-items: center;\n'
                    '    justify-content: space-between;\n'
                    '    padding: 0 2rem;\n'
                    '    height: 64px;\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Animated gradient border',
                'code': (
                    '@keyframes rotate {\n'
                    '    from { transform: rotate(0deg); }\n'
                    '    to   { transform: rotate(360deg); }\n'
                    '}\n'
                    '.gradient-border {\n'
                    '    position: relative;\n'
                    '    border-radius: 12px;\n'
                    '    overflow: hidden;\n'
                    '    padding: 2px;\n'
                    '}\n'
                    '.gradient-border::before {\n'
                    '    content: "";\n'
                    '    position: absolute;\n'
                    '    inset: -50%;\n'
                    '    background: conic-gradient(#6c63ff, #e040fb, #00bcd4, #6c63ff);\n'
                    '    animation: rotate 3s linear infinite;\n'
                    '}\n'
                    '.gradient-border-inner {\n'
                    '    position: relative;\n'
                    '    background: #0f0f1a;\n'
                    '    border-radius: 10px;\n'
                    '    padding: 1.5rem;\n'
                    '}\n'
                ),
            },
            {
                'title': 'CSS scroll-driven animation',
                'code': (
                    '@keyframes fade-in {\n'
                    '    from { opacity: 0; transform: translateY(20px); }\n'
                    '    to   { opacity: 1; transform: translateY(0); }\n'
                    '}\n'
                    '.reveal {\n'
                    '    animation: fade-in linear both;\n'
                    '    animation-timeline: view();\n'
                    '    animation-range: entry 0% entry 30%;\n'
                    '}\n'
                    '.stagger > * {\n'
                    '    animation: fade-in linear both;\n'
                    '    animation-timeline: view();\n'
                    '    animation-range: entry 0% entry 25%;\n'
                    '}\n'
                    '.stagger > *:nth-child(2) { animation-delay: 80ms; }\n'
                    '.stagger > *:nth-child(3) { animation-delay: 160ms; }\n'
                    '.stagger > *:nth-child(4) { animation-delay: 240ms; }\n'
                ),
            },
            {
                'title': 'Neon glow effect',
                'code': (
                    ':root {\n'
                    '    --neon: #00ffcc;\n'
                    '    --neon-glow: 0 0 7px var(--neon),\n'
                    '                 0 0 14px var(--neon),\n'
                    '                 0 0 28px var(--neon),\n'
                    '                 0 0 56px rgba(0,255,204,.4);\n'
                    '}\n'
                    '.neon-text {\n'
                    '    color: var(--neon);\n'
                    '    text-shadow: var(--neon-glow);\n'
                    '    animation: flicker 2.5s infinite alternate;\n'
                    '}\n'
                    '@keyframes flicker {\n'
                    '    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {\n'
                    '        text-shadow: var(--neon-glow);\n'
                    '    }\n'
                    '    20%, 24%, 55% {\n'
                    '        text-shadow: none;\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed the database with programming languages and code snippets'

    def handle(self, *args, **options):
        self.stdout.write('Seeding languages...')
        lang_objects = {}
        for lang_data in LANGUAGES:
            lang, created = Language.objects.update_or_create(
                slug=lang_data['slug'],
                defaults={'name': lang_data['name'], 'icon': lang_data['icon']},
            )
            lang_objects[lang_data['slug']] = lang
            if created:
                self.stdout.write(f'  Created language: {lang.name}')

        self.stdout.write('Seeding snippets...')
        total = 0
        for lang_slug, difficulties in SNIPPETS.items():
            lang = lang_objects[lang_slug]
            for difficulty, snippets in difficulties.items():
                for s_data in snippets:
                    snippet, created = Snippet.objects.update_or_create(
                        language=lang,
                        difficulty=difficulty,
                        title=s_data['title'],
                        defaults={'code': s_data['code']},
                    )
                    if created:
                        total += 1

        self.stdout.write(self.style.SUCCESS(f'Done! Created {total} new snippets.'))

