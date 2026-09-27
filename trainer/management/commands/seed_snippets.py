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
    {'slug': 'bash',       'name': 'Bash',                  'icon': '🐚'},
    {'slug': 'html',       'name': 'HTML',                  'icon': '🌐'},
    {'slug': 'php',        'name': 'PHP',                   'icon': '🐘'},
    {'slug': 'csharp',     'name': 'C#',                    'icon': '🎯'},
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
    'bash': {
        'easy': [
            {
                'title': 'Ensure directory exists',
                'code': (
                    'if [ ! -d "$TARGET_DIR" ]; then\n'
                    '    echo "Creating directory: $TARGET_DIR"\n'
                    '    mkdir -p "$TARGET_DIR"\n'
                    'else\n'
                    '    echo "Directory already exists: $TARGET_DIR"\n'
                    'fi\n'
                ),
            },
            {
                'title': 'Loop over log files',
                'code': (
                    'for file in "$LOG_DIR"/*.log; do\n'
                    '    [ -f "$file" ] || continue\n'
                    '    filename=$(basename "$file")\n'
                    '    echo "Compressing: $filename"\n'
                    '    gzip -c "$file" > "${BACKUP_DIR}/${filename}.gz"\n'
                    'done\n'
                ),
            },
            {
                'title': 'Validate script arguments',
                'code': (
                    'if [ "$#" -lt 2 ]; then\n'
                    '    echo "Usage: $0 <source_file> <target_file>"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'SOURCE="$1"\n'
                    'TARGET="$2"\n'
                    'cp -v "$SOURCE" "$TARGET"\n'
                ),
            },
            {
                'title': 'Read config line by line',
                'code': (
                    'while IFS= read -r line || [ -n "$line" ]; do\n'
                    '    [[ "$line" =~ ^#.*$ ]] && continue\n'
                    '    [ -z "$line" ] && continue\n'
                    '    echo "Config entry: $line"\n'
                    'done < "app.env"\n'
                ),
            },
            {
                'title': 'Timestamped backup function',
                'code': (
                    'backup_file() {\n'
                    '    local src="$1"\n'
                    '    local timestamp\n'
                    '    timestamp=$(date +"%Y%m%d_%H%M%S")\n'
                    '    local dest="${src}.bak_${timestamp}"\n'
                    '    cp -a "$src" "$dest"\n'
                    '    echo "Backup saved: $dest"\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Strict preamble & cleanup trap',
                'code': (
                    'set -euo pipefail\n'
                    'IFS=$\'\\n\\t\'\n'
                    '\n'
                    'TMP_DIR=$(mktemp -d)\n'
                    'cleanup() {\n'
                    '    echo "Removing temporary directory..."\n'
                    '    rm -rf "$TMP_DIR"\n'
                    '}\n'
                    'trap cleanup EXIT INT TERM\n'
                    '\n'
                    'echo "Executing task inside $TMP_DIR"\n'
                ),
            },
            {
                'title': 'Exponential backoff retry',
                'code': (
                    'retry_command() {\n'
                    '    local max_attempts=5\n'
                    '    local delay=2\n'
                    '    local attempt=1\n'
                    '\n'
                    '    while [ $attempt -le $max_attempts ]; do\n'
                    '        if "$@"; then\n'
                    '            return 0\n'
                    '        fi\n'
                    '        echo "Attempt $attempt failed. Waiting ${delay}s..."\n'
                    '        sleep $delay\n'
                    '        delay=$((delay * 2))\n'
                    '        attempt=$((attempt + 1))\n'
                    '    done\n'
                    '    return 1\n'
                    '}\n'
                ),
            },
            {
                'title': 'Parse CLI flags with getopts',
                'code': (
                    'VERBOSE=false\n'
                    'OUTPUT=""\n'
                    '\n'
                    'while getopts ":hvo:" opt; do\n'
                    '    case "$opt" in\n'
                    '        v) VERBOSE=true ;;\n'
                    '        o) OUTPUT="$OPTARG" ;;\n'
                    '        h)\n'
                    '            echo "Usage: $0 [-v] [-o output_file]"\n'
                    '            exit 0\n'
                    '            ;;\n'
                    '        \\?)\n'
                    '            echo "Invalid option: -$OPTARG" >&2\n'
                    '            exit 1\n'
                    '            ;;\n'
                    '    esac\n'
                    'done\n'
                    'shift $((OPTIND - 1))\n'
                ),
            },
            {
                'title': 'Check required dependencies',
                'code': (
                    'check_dependencies() {\n'
                    '    local deps=("curl" "jq" "git" "tar")\n'
                    '    local missing=()\n'
                    '\n'
                    '    for cmd in "${deps[@]}"; do\n'
                    '        if ! command -v "$cmd" >/dev/null 2>&1; then\n'
                    '            missing+=("$cmd")\n'
                    '        fi\n'
                    '    done\n'
                    '\n'
                    '    if [ ${#missing[@]} -gt 0 ]; then\n'
                    '        echo "Missing required dependencies: ${missing[*]}" >&2\n'
                    '        exit 1\n'
                    '    fi\n'
                    '}\n'
                ),
            },
            {
                'title': 'Interactive confirmation prompt',
                'code': (
                    'confirm_action() {\n'
                    '    local prompt="${1:-Continue?}"\n'
                    '    local default="${2:-N}"\n'
                    '    local reply\n'
                    '\n'
                    '    read -r -p "$prompt [y/N]: " reply\n'
                    '    reply="${reply:-$default}"\n'
                    '\n'
                    '    case "$reply" in\n'
                    '        [yY][eE][sS]|[yY]) return 0 ;;\n'
                    '        *) return 1 ;;\n'
                    '    esac\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Terminal progress spinner',
                'code': (
                    'run_with_spinner() {\n'
                    '    local pid=$1\n'
                    '    local delay=0.1\n'
                    '    local spinstr=\'|/-\\\'\n'
                    '    tput civis\n'
                    '\n'
                    '    while kill -0 "$pid" 2>/dev/null; do\n'
                    '        local temp=${spinstr#?}\n'
                    '        printf " [%c]  " "$spinstr"\n'
                    '        spinstr=$temp${spinstr%"$temp"}\n'
                    '        sleep $delay\n'
                    '        printf "\\b\\b\\b\\b\\b\\b"\n'
                    '    done\n'
                    '\n'
                    '    printf "    \\b\\b\\b\\b"\n'
                    '    tput cnorm\n'
                    '    wait "$pid"\n'
                    '    return $?\n'
                    '}\n'
                ),
            },
            {
                'title': 'Parallel task execution queue',
                'code': (
                    'run_parallel_jobs() {\n'
                    '    local max_jobs=4\n'
                    '    local current_jobs=0\n'
                    '\n'
                    '    for task in "$@"; do\n'
                    '        bash -c "$task" &\n'
                    '        current_jobs=$((current_jobs + 1))\n'
                    '\n'
                    '        if [ "$current_jobs" -ge "$max_jobs" ]; then\n'
                    '            wait -n\n'
                    '            current_jobs=$((current_jobs - 1))\n'
                    '        fi\n'
                    '    done\n'
                    '    wait\n'
                    '    echo "All batch tasks completed."\n'
                    '}\n'
                ),
            },
            {
                'title': 'Colorized structured logger',
                'code': (
                    'log_message() {\n'
                    '    local level="$1"\n'
                    '    shift\n'
                    '    local timestamp\n'
                    '    timestamp=$(date +"%Y-%m-%d %H:%M:%S")\n'
                    '\n'
                    '    local RED=\'\\033[0;31m\'\n'
                    '    local GREEN=\'\\033[0;32m\'\n'
                    '    local YELLOW=\'\\033[1;33m\'\n'
                    '    local BLUE=\'\\033[0;34m\'\n'
                    '    local NC=\'\\033[0m\'\n'
                    '\n'
                    '    case "$level" in\n'
                    '        INFO)  printf "%b[%s] [INFO]%b  %s\\n" "$BLUE" "$timestamp" "$NC" "$*" ;;\n'
                    '        WARN)  printf "%b[%s] [WARN]%b  %s\\n" "$YELLOW" "$timestamp" "$NC" "$*" ;;\n'
                    '        ERROR) printf "%b[%s] [ERROR]%b %s\\n" "$RED" "$timestamp" "$NC" "$*" >&2 ;;\n'
                    '        OK)    printf "%b[%s] [OK]%b    %s\\n" "$GREEN" "$timestamp" "$NC" "$*" ;;\n'
                    '    esac\n'
                    '}\n'
                ),
            },
            {
                'title': 'Disk partition usage audit',
                'code': (
                    'check_disk_health() {\n'
                    '    local threshold=85\n'
                    '    local alert=false\n'
                    '\n'
                    '    while IFS= read -r partition; do\n'
                    '        local usage\n'
                    '        usage=$(echo "$partition" | awk \'{print $5}\' | tr -d \'%\')\n'
                    '        local mount\n'
                    '        mount=$(echo "$partition" | awk \'{print $6}\')\n'
                    '\n'
                    '        if [ "$usage" -ge "$threshold" ]; then\n'
                    '            echo "ALERT: Partition $mount is at ${usage}% capacity!" >&2\n'
                    '            alert=true\n'
                    '        fi\n'
                    '    done < <(df -h -x tmpfs -x devtmpfs | tail -n +2)\n'
                    '\n'
                    '    [ "$alert" = false ]\n'
                    '}\n'
                ),
            },
            {
                'title': 'Safe JSON value extractor',
                'code': (
                    'extract_json_key() {\n'
                    '    local json_input="$1"\n'
                    '    local target_key="$2"\n'
                    '\n'
                    '    if command -v jq >/dev/null 2>&1; then\n'
                    '        echo "$json_input" | jq -r ".${target_key} // empty"\n'
                    '    elif command -v python3 >/dev/null 2>&1; then\n'
                    '        python3 -c "import sys, json; doc = json.loads(sys.argv[1]); print(doc.get(sys.argv[2], \'\'))" "$json_input" "$target_key"\n'
                    '    else\n'
                    '        echo "Neither jq nor python3 found for JSON parsing" >&2\n'
                    '        return 1\n'
                    '    fi\n'
                    '}\n'
                ),
            },
        ],
    },

    'html': {
        'easy': [
            {
                'title': 'Card component',
                'code': (
                    '<article class="card">\n'
                    '  <img src="avatar.jpg" alt="User avatar" class="card-avatar" />\n'
                    '  <div class="card-body">\n'
                    '    <h3 class="card-title">John Doe</h3>\n'
                    '    <p class="card-role">Software Architect</p>\n'
                    '    <a href="#profile" class="btn-link">View Profile</a>\n'
                    '  </div>\n'
                    '</article>\n'
                ),
            },
            {
                'title': 'Search form with label',
                'code': (
                    '<form role="search" class="search-form" action="/search" method="get">\n'
                    '  <label for="site-search" class="visually-hidden">Search site:</label>\n'
                    '  <input type="search" id="site-search" name="q" placeholder="Search docs..." required />\n'
                    '  <button type="submit" aria-label="Submit search">\n'
                    '    <span class="icon">🔍</span>\n'
                    '  </button>\n'
                    '</form>\n'
                ),
            },
            {
                'title': 'Audio player with fallbacks',
                'code': (
                    '<figure class="audio-widget">\n'
                    '  <figcaption>Episode 42: Building High-Performance APIs</figcaption>\n'
                    '  <audio controls preload="metadata">\n'
                    '    <source src="podcast-ep42.mp3" type="audio/mpeg" />\n'
                    '    <source src="podcast-ep42.ogg" type="audio/ogg" />\n'
                    '    <p>Your browser does not support HTML5 audio.</p>\n'
                    '  </audio>\n'
                    '</figure>\n'
                ),
            },
            {
                'title': 'Responsive picture element',
                'code': (
                    '<picture class="hero-picture">\n'
                    '  <source srcset="hero-large.avif" type="image/avif" media="(min-width: 1024px)" />\n'
                    '  <source srcset="hero-medium.webp" type="image/webp" media="(min-width: 640px)" />\n'
                    '  <img src="hero-fallback.jpg" alt="Modern workspace setup" loading="lazy" width="800" height="450" />\n'
                    '</picture>\n'
                ),
            },
            {
                'title': 'Interactive details disclosure',
                'code': (
                    '<details class="faq-item">\n'
                    '  <summary class="faq-question">What languages are supported?</summary>\n'
                    '  <div class="faq-answer">\n'
                    '    <p>SprintCoder supports Python, JavaScript, Java, C++, Go, SQL, CSS, Bash, HTML, PHP, and C#.</p>\n'
                    '  </div>\n'
                    '</details>\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'Billing address form',
                'code': (
                    '<fieldset class="billing-fieldset">\n'
                    '  <legend>Billing Address</legend>\n'
                    '  <div class="form-row">\n'
                    '    <label for="first-name">First Name</label>\n'
                    '    <input type="text" id="first-name" name="firstName" autocomplete="given-name" required />\n'
                    '  </div>\n'
                    '  <div class="form-row">\n'
                    '    <label for="last-name">Last Name</label>\n'
                    '    <input type="text" id="last-name" name="lastName" autocomplete="family-name" required />\n'
                    '  </div>\n'
                    '  <div class="form-row">\n'
                    '    <label for="email">Work Email</label>\n'
                    '    <input type="email" id="email" name="email" autocomplete="email" required />\n'
                    '  </div>\n'
                    '  <div class="form-row">\n'
                    '    <label for="country">Country</label>\n'
                    '    <select id="country" name="country" required>\n'
                    '      <option value="">Select country...</option>\n'
                    '      <option value="US">United States</option>\n'
                    '      <option value="DE">Germany</option>\n'
                    '      <option value="JP">Japan</option>\n'
                    '    </select>\n'
                    '  </div>\n'
                    '</fieldset>\n'
                ),
            },
            {
                'title': 'Semantic responsive header',
                'code': (
                    '<header class="primary-header">\n'
                    '  <a href="/" class="brand-logo" aria-label="Homepage">\n'
                    '    <svg width="32" height="32" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>\n'
                    '    <span class="brand-name">SprintCoder</span>\n'
                    '  </a>\n'
                    '  <nav class="site-navigation" aria-label="Primary navigation">\n'
                    '    <ul class="nav-list">\n'
                    '      <li><a href="/practice" class="nav-link active" aria-current="page">Practice</a></li>\n'
                    '      <li><a href="/leaderboard" class="nav-link">Leaderboard</a></li>\n'
                    '      <li><a href="/snippets" class="nav-link">Snippets</a></li>\n'
                    '      <li><a href="/profile" class="nav-link">Profile</a></li>\n'
                    '    </ul>\n'
                    '  </nav>\n'
                    '  <div class="header-actions">\n'
                    '    <button type="button" class="btn btn-secondary">Settings</button>\n'
                    '  </div>\n'
                    '</header>\n'
                ),
            },
            {
                'title': 'Accessible modal dialog',
                'code': (
                    '<dialog id="confirm-modal" class="modal" aria-labelledby="modal-title">\n'
                    '  <form method="dialog" class="modal-box">\n'
                    '    <header class="modal-header">\n'
                    '      <h2 id="modal-title">Delete Snippet</h2>\n'
                    '      <button type="submit" value="cancel" class="btn-close" aria-label="Close modal">✕</button>\n'
                    '    </header>\n'
                    '    <div class="modal-content">\n'
                    '      <p>Are you sure you want to permanently delete this practice snippet?</p>\n'
                    '      <p class="text-warning">This action cannot be undone.</p>\n'
                    '    </div>\n'
                    '    <footer class="modal-footer">\n'
                    '      <button type="submit" value="cancel" class="btn btn-ghost">Cancel</button>\n'
                    '      <button type="submit" value="confirm" class="btn btn-danger">Delete</button>\n'
                    '    </footer>\n'
                    '  </form>\n'
                    '</dialog>\n'
                ),
            },
            {
                'title': 'Pricing tier card',
                'code': (
                    '<div class="pricing-card highlighted">\n'
                    '  <div class="card-badge">Most Popular</div>\n'
                    '  <h3 class="tier-name">Pro Developer</h3>\n'
                    '  <div class="tier-price">\n'
                    '    <span class="currency">$</span>\n'
                    '    <span class="amount">19</span>\n'
                    '    <span class="period">/month</span>\n'
                    '  </div>\n'
                    '  <ul class="tier-features" role="list">\n'
                    '    <li>✓ Unlimited practice sessions</li>\n'
                    '    <li>✓ Personal GitHub repo sync</li>\n'
                    '    <li>✓ Detailed speed analytics</li>\n'
                    '    <li>✓ Custom theme designer</li>\n'
                    '  </ul>\n'
                    '  <button type="button" class="btn btn-primary btn-block">Upgrade to Pro</button>\n'
                    '</div>\n'
                ),
            },
            {
                'title': 'Stats overview tiles',
                'code': (
                    '<section class="stats-overview" aria-label="Performance Metrics">\n'
                    '  <div class="stat-tile">\n'
                    '    <span class="stat-icon" aria-hidden="true">⚡</span>\n'
                    '    <span class="stat-title">Peak Speed</span>\n'
                    '    <strong class="stat-number">124 <small>WPM</small></strong>\n'
                    '    <span class="stat-delta positive">+12% this week</span>\n'
                    '  </div>\n'
                    '  <div class="stat-tile">\n'
                    '    <span class="stat-icon" aria-hidden="true">🎯</span>\n'
                    '    <span class="stat-title">Accuracy</span>\n'
                    '    <strong class="stat-number">99.2<small>%</small></strong>\n'
                    '    <span class="stat-delta neutral">Target: 98%</span>\n'
                    '  </div>\n'
                    '</section>\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Full semantic page layout',
                'code': (
                    '<!DOCTYPE html>\n'
                    '<html lang="en" data-theme="dark">\n'
                    '<head>\n'
                    '  <meta charset="UTF-8" />\n'
                    '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
                    '  <meta name="description" content="SprintCoder - Developer Typing Speed Trainer" />\n'
                    '  <title>Developer Typing Arena</title>\n'
                    '  <link rel="stylesheet" href="/styles/main.css" />\n'
                    '  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />\n'
                    '</head>\n'
                    '<body>\n'
                    '  <div class="app-layout">\n'
                    '    <aside class="sidebar" aria-label="Sidebar navigation">\n'
                    '      <nav class="sidebar-nav">\n'
                    '        <a href="#dashboard" class="sidebar-item active">Dashboard</a>\n'
                    '        <a href="#training" class="sidebar-item">Training</a>\n'
                    '        <a href="#stats" class="sidebar-item">Statistics</a>\n'
                    '      </nav>\n'
                    '    </aside>\n'
                    '    <main id="main-content" class="content-area">\n'
                    '      <section class="hero-banner">\n'
                    '        <h1>Master Every Keystroke</h1>\n'
                    '        <p>Real syntax training for professional software engineers.</p>\n'
                    '        <div class="cta-group">\n'
                    '          <button class="btn btn-accent">Start Session</button>\n'
                    '          <a href="#learn-more" class="btn btn-outline">Documentation</a>\n'
                    '        </div>\n'
                    '      </section>\n'
                    '    </main>\n'
                    '  </div>\n'
                    '</body>\n'
                    '</html>\n'
                ),
            },
            {
                'title': 'Results benchmark table',
                'code': (
                    '<div class="table-container" tabindex="0" role="region" aria-label="Attempt Results">\n'
                    '  <table class="data-table">\n'
                    '    <caption>Typing benchmark results sorted by highest WPM</caption>\n'
                    '    <thead>\n'
                    '      <tr>\n'
                    '        <th scope="col">Language</th>\n'
                    '        <th scope="col">Difficulty</th>\n'
                    '        <th scope="col" class="num-col">WPM</th>\n'
                    '        <th scope="col" class="num-col">CPM</th>\n'
                    '        <th scope="col" class="num-col">Accuracy</th>\n'
                    '        <th scope="col" class="num-col">Duration</th>\n'
                    '      </tr>\n'
                    '    </thead>\n'
                    '    <tbody>\n'
                    '      <tr>\n'
                    '        <th scope="row"><span class="badge lang-py">Python</span></th>\n'
                    '        <td><span class="diff-tag medium">Medium</span></td>\n'
                    '        <td class="num-col"><strong>92.4</strong></td>\n'
                    '        <td class="num-col">462</td>\n'
                    '        <td class="num-col success">99.1%</td>\n'
                    '        <td class="num-col">45.2s</td>\n'
                    '      </tr>\n'
                    '      <tr>\n'
                    '        <th scope="row"><span class="badge lang-js">JavaScript</span></th>\n'
                    '        <td><span class="diff-tag hard">Hard</span></td>\n'
                    '        <td class="num-col"><strong>88.0</strong></td>\n'
                    '        <td class="num-col">440</td>\n'
                    '        <td class="num-col success">97.8%</td>\n'
                    '        <td class="num-col">62.0s</td>\n'
                    '      </tr>\n'
                    '    </tbody>\n'
                    '  </table>\n'
                    '</div>\n'
                ),
            },
            {
                'title': 'Multi-step signup wizard',
                'code': (
                    '<form class="multi-step-form" id="signup-wizard">\n'
                    '  <nav class="steps-progress" aria-label="Registration steps">\n'
                    '    <ol class="step-indicators">\n'
                    '      <li class="step completed" aria-current="false">\n'
                    '        <span class="step-number">1</span>\n'
                    '        <span class="step-label">Account</span>\n'
                    '      </li>\n'
                    '      <li class="step current" aria-current="step">\n'
                    '        <span class="step-number">2</span>\n'
                    '        <span class="step-label">Preferences</span>\n'
                    '      </li>\n'
                    '      <li class="step" aria-current="false">\n'
                    '        <span class="step-number">3</span>\n'
                    '        <span class="step-label">Confirm</span>\n'
                    '      </li>\n'
                    '    </ol>\n'
                    '  </nav>\n'
                    '  <div class="step-content">\n'
                    '    <fieldset class="preferences-box">\n'
                    '      <legend>Editor Preferences</legend>\n'
                    '      <div class="field-group">\n'
                    '        <label for="font-family">Default Code Font</label>\n'
                    '        <select id="font-family" name="fontFamily">\n'
                    '          <option value="jetbrains">JetBrains Mono</option>\n'
                    '          <option value="fira">Fira Code</option>\n'
                    '          <option value="roboto">Roboto Mono</option>\n'
                    '        </select>\n'
                    '      </div>\n'
                    '    </fieldset>\n'
                    '  </div>\n'
                    '</form>\n'
                ),
            },
            {
                'title': 'Playground dual pane layout',
                'code': (
                    '<section class="playground-grid" aria-label="Interactive Code Playground">\n'
                    '  <div class="pane editor-pane">\n'
                    '    <div class="pane-bar">\n'
                    '      <span class="pane-tab active">index.html</span>\n'
                    '      <span class="pane-tab">styles.css</span>\n'
                    '    </div>\n'
                    '    <div class="editor-surface" role="textbox" aria-multiline="true">\n'
                    '      <pre><code>&lt;button class="btn"&gt;Click me&lt;/button&gt;</code></pre>\n'
                    '    </div>\n'
                    '  </div>\n'
                    '  <div class="pane preview-pane">\n'
                    '    <div class="pane-bar">\n'
                    '      <span class="pane-title">Live Preview</span>\n'
                    '      <button class="btn-refresh" aria-label="Refresh preview">🔄</button>\n'
                    '    </div>\n'
                    '    <iframe src="about:blank" title="Preview Frame" class="preview-frame" sandbox="allow-scripts"></iframe>\n'
                    '  </div>\n'
                    '</section>\n'
                ),
            },
            {
                'title': 'User profile card with bio',
                'code': (
                    '<div class="profile-card-full">\n'
                    '  <div class="profile-cover" style="background-image: url(\'/cover.jpg\');"></div>\n'
                    '  <div class="profile-header-strip">\n'
                    '    <img src="/avatar.jpg" alt="Profile of Alice" class="avatar-large" />\n'
                    '    <div class="header-titles">\n'
                    '      <h2>Alice Vance</h2>\n'
                    '      <p class="handle">@alice_dev &bull; Joined March 2024</p>\n'
                    '    </div>\n'
                    '    <div class="profile-cta">\n'
                    '      <button type="button" class="btn btn-primary">Follow</button>\n'
                    '      <button type="button" class="btn btn-icon" aria-label="More options">•••</button>\n'
                    '    </div>\n'
                    '  </div>\n'
                    '  <div class="profile-bio">\n'
                    '    <p>Full-stack developer building developer tools and reactive web interfaces.</p>\n'
                    '    <ul class="meta-list" role="list">\n'
                    '      <li>📍 Berlin, Germany</li>\n'
                    '      <li>🔗 <a href="https://example.com">alice.dev</a></li>\n'
                    '      <li>💼 Freelance Engineer</li>\n'
                    '    </ul>\n'
                    '  </div>\n'
                    '</div>\n'
                ),
            },
        ],
    },
    'php': {
        'easy': [
            {
                'title': 'Filter even numbers',
                'code': (
                    'function getEvenNumbers(array $numbers): array {\n'
                    '    return array_values(array_filter(\n'
                    '        $numbers,\n'
                    '        fn(int $n): bool => $n % 2 === 0\n'
                    '    ));\n'
                    '}\n'
                    '\n'
                    '$evens = getEvenNumbers([1, 2, 3, 4, 5, 6, 7, 8]);\n'
                ),
            },
            {
                'title': 'String slugifier',
                'code': (
                    'function slugify(string $text): string {\n'
                    '    $text = preg_replace(\'~[^\\pL\\d]+~u\', \'-\', $text);\n'
                    '    $text = iconv(\'utf-8\', \'us-ascii//TRANSLIT\', $text);\n'
                    '    $text = preg_replace(\'~[^-\\w]+~\', \'\', $text);\n'
                    '    return strtolower(trim($text, \'-\'));\n'
                    '}\n'
                ),
            },
            {
                'title': 'Read environment variable',
                'code': (
                    'function env(string $key, mixed $default = null): mixed {\n'
                    '    $value = getenv($key);\n'
                    '    if ($value === false) {\n'
                    '        return $default;\n'
                    '    }\n'
                    '    return match (strtolower($value)) {\n'
                    '        \'true\' => true,\n'
                    '        \'false\' => false,\n'
                    '        \'null\' => null,\n'
                    '        default => $value,\n'
                    '    };\n'
                    '}\n'
                ),
            },
            {
                'title': 'Email Value Object',
                'code': (
                    'final readonly class EmailAddress {\n'
                    '    public function __construct(public string $value) {\n'
                    '        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {\n'
                    '            throw new InvalidArgumentException("Invalid email: {$value}");\n'
                    '        }\n'
                    '    }\n'
                    '\n'
                    '    public function getDomain(): string {\n'
                    '        return substr(strrchr($this->value, \'@\'), 1);\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'JSON response helper',
                'code': (
                    'function jsonResponse(mixed $data, int $status = 200): void {\n'
                    '    http_response_code($status);\n'
                    '    header(\'Content-Type: application/json; charset=utf-8\');\n'
                    '    echo json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES);\n'
                    '    exit;\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'PDO Database Singleton',
                'code': (
                    'final class Database {\n'
                    '    private static ?PDO $instance = null;\n'
                    '\n'
                    '    public static function getConnection(): PDO {\n'
                    '        if (self::$instance === null) {\n'
                    '            $dsn = \'mysql:host=127.0.0.1;dbname=app;charset=utf8mb4\';\n'
                    '            self::$instance = new PDO($dsn, \'db_user\', \'secret\', [\n'
                    '                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,\n'
                    '                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,\n'
                    '                PDO::ATTR_EMULATE_PREPARES => false,\n'
                    '            ]);\n'
                    '        }\n'
                    '        return self::$instance;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'User repository pattern',
                'code': (
                    'final class UserRepository {\n'
                    '    public function __construct(private PDO $db) {}\n'
                    '\n'
                    '    public function findByEmail(string $email): ?User {\n'
                    '        $stmt = $this->db->prepare(\'SELECT * FROM users WHERE email = :email LIMIT 1\');\n'
                    '        $stmt->execute([\'email\' => $email]);\n'
                    '        $row = $stmt->fetch();\n'
                    '\n'
                    '        if (!$row) {\n'
                    '            return null;\n'
                    '        }\n'
                    '\n'
                    '        return new User(\n'
                    '            id: (int) $row[\'id\'],\n'
                    '            name: $row[\'name\'],\n'
                    '            email: $row[\'email\'],\n'
                    '            createdAt: new DateTimeImmutable($row[\'created_at\'])\n'
                    '        );\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'API Bearer auth middleware',
                'code': (
                    'final class AuthenticationMiddleware {\n'
                    '    public function handle(Request $request, callable $next): Response {\n'
                    '        $token = $request->getHeaderLine(\'Authorization\');\n'
                    '\n'
                    '        if (!str_starts_with($token, \'Bearer \')) {\n'
                    '            return new JsonResponse([\'error\' => \'Unauthorized\'], 401);\n'
                    '        }\n'
                    '\n'
                    '        $apiKey = substr($token, 7);\n'
                    '        if (!$this->isValidApiKey($apiKey)) {\n'
                    '            return new JsonResponse([\'error\' => \'Invalid token\'], 403);\n'
                    '        }\n'
                    '\n'
                    '        return $next($request);\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Redis token rate limiter',
                'code': (
                    'final class RateLimiter {\n'
                    '    public function __construct(\n'
                    '        private Redis $redis,\n'
                    '        private int $maxAttempts = 60,\n'
                    '        private int $decaySeconds = 60\n'
                    '    ) {}\n'
                    '\n'
                    '    public function tooManyAttempts(string $key): bool {\n'
                    '        $attempts = (int) $this->redis->get($key);\n'
                    '        return $attempts >= $this->maxAttempts;\n'
                    '    }\n'
                    '\n'
                    '    public function hit(string $key): int {\n'
                    '        $count = $this->redis->incr($key);\n'
                    '        if ($count === 1) {\n'
                    '            $this->redis->expire($key, $this->decaySeconds);\n'
                    '        }\n'
                    '        return $count;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Expiring file cache store',
                'code': (
                    'final class SimpleCache {\n'
                    '    public function __construct(private string $cacheDir) {}\n'
                    '\n'
                    '    public function set(string $key, mixed $value, int $ttl = 3600): bool {\n'
                    '        $filename = $this->cacheDir . \'/\' . md5($key) . \'.cache\';\n'
                    '        $payload = serialize([\n'
                    '            \'expires\' => time() + $ttl,\n'
                    '            \'data\' => $value,\n'
                    '        ]);\n'
                    '        return file_put_contents($filename, $payload, LOCK_EX) !== false;\n'
                    '    }\n'
                    '\n'
                    '    public function get(string $key, mixed $default = null): mixed {\n'
                    '        $filename = $this->cacheDir . \'/\' . md5($key) . \'.cache\';\n'
                    '        if (!file_exists($filename)) return $default;\n'
                    '        $content = unserialize(file_get_contents($filename));\n'
                    '        if ($content[\'expires\'] < time()) {\n'
                    '            unlink($filename);\n'
                    '            return $default;\n'
                    '        }\n'
                    '        return $content[\'data\'];\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Event dispatcher with typed events',
                'code': (
                    'final class EventDispatcher {\n'
                    '    /** @var array<string, list<callable>> */\n'
                    '    private array $listeners = [];\n'
                    '\n'
                    '    public function listen(string $eventClass, callable $listener): void {\n'
                    '        $this->listeners[$eventClass][] = $listener;\n'
                    '    }\n'
                    '\n'
                    '    public function dispatch(object $event): object {\n'
                    '        $eventClass = get_class($event);\n'
                    '        if (!isset($this->listeners[$eventClass])) {\n'
                    '            return $event;\n'
                    '        }\n'
                    '\n'
                    '        foreach ($this->listeners[$eventClass] as $listener) {\n'
                    '            $listener($event);\n'
                    '            if ($event instanceof StoppableEventInterface && $event->isPropagationStopped()) {\n'
                    '                break;\n'
                    '            }\n'
                    '        }\n'
                    '\n'
                    '        return $event;\n'
                    '    }\n'
                    '}\n'
                    '\n'
                    'final class UserRegisteredEvent {\n'
                    '    public function __construct(\n'
                    '        public readonly int $userId,\n'
                    '        public readonly string $email,\n'
                    '        public readonly DateTimeImmutable $occurredAt = new DateTimeImmutable()\n'
                    '    ) {}\n'
                    '}\n'
                ),
            },
            {
                'title': 'Micro HTTP regex router',
                'code': (
                    'final class Router {\n'
                    '    private array $routes = [];\n'
                    '\n'
                    '    public function add(string $method, string $path, callable $handler): void {\n'
                    '        $pattern = preg_replace(\'/\\{([a-zA-Z0-9_]+)\\}/\', \'(?P<$1>[^/]+)\', $path);\n'
                    '        $this->routes[] = [\n'
                    '            \'method\' => strtoupper($method),\n'
                    '            \'pattern\' => \'#^\' . $pattern . \'$#\',\n'
                    '            \'handler\' => $handler,\n'
                    '        ];\n'
                    '    }\n'
                    '\n'
                    '    public function dispatch(string $method, string $uri): mixed {\n'
                    '        $path = parse_url($uri, PHP_URL_PATH);\n'
                    '        foreach ($this->routes as $route) {\n'
                    '            if ($route[\'method\'] !== $method) continue;\n'
                    '            if (preg_match($route[\'pattern\'], $path, $matches)) {\n'
                    '                $params = array_filter($matches, \'is_string\', ARRAY_FILTER_USE_KEY);\n'
                    '                return call_user_func($route[\'handler\'], $params);\n'
                    '            }\n'
                    '        }\n'
                    '        http_response_code(404);\n'
                    '        return [\'error\' => \'Route not found\'];\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Transactional command bus',
                'code': (
                    'interface CommandHandlerInterface {\n'
                    '    public function handle(object $command): void;\n'
                    '}\n'
                    '\n'
                    'final class TransactionalCommandBus {\n'
                    '    public function __construct(\n'
                    '        private PDO $db,\n'
                    '        private array $handlers = []\n'
                    '    ) {}\n'
                    '\n'
                    '    public function register(string $commandClass, CommandHandlerInterface $handler): void {\n'
                    '        $this->handlers[$commandClass] = $handler;\n'
                    '    }\n'
                    '\n'
                    '    public function execute(object $command): void {\n'
                    '        $class = get_class($command);\n'
                    '        if (!isset($this->handlers[$class])) {\n'
                    '            throw new RuntimeException("No handler registered for command {$class}");\n'
                    '        }\n'
                    '\n'
                    '        $this->db->beginTransaction();\n'
                    '        try {\n'
                    '            $this->handlers[$class]->handle($command);\n'
                    '            $this->db->commit();\n'
                    '        } catch (Throwable $e) {\n'
                    '            $this->db->rollBack();\n'
                    '            throw $e;\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'CSV output streaming exporter',
                'code': (
                    'final class CsvStreamExporter {\n'
                    '    public function __construct(private PDOStatement $statement) {}\n'
                    '\n'
                    '    public function exportToOutput(string $filename): void {\n'
                    '        header(\'Content-Type: text/csv; charset=utf-8\');\n'
                    '        header(\'Content-Disposition: attachment; filename="\' . $filename . \'"\');\n'
                    '        header(\'Pragma: no-cache\');\n'
                    '        header(\'Expires: 0\');\n'
                    '\n'
                    '        $output = fopen(\'php://output\', \'w\');\n'
                    '        fputs($output, "\xEF\xBB\xBF");\n'
                    '\n'
                    '        $headersWritten = false;\n'
                    '        while ($row = $this->statement->fetch(PDO::FETCH_ASSOC)) {\n'
                    '            if (!$headersWritten) {\n'
                    '                fputcsv($output, array_keys($row));\n'
                    '                $headersWritten = true;\n'
                    '            }\n'
                    '            fputcsv($output, $row);\n'
                    '        }\n'
                    '\n'
                    '        fclose($output);\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'HMAC JWT encoder and validator',
                'code': (
                    'final class JwtService {\n'
                    '    public function __construct(private string $secretKey) {}\n'
                    '\n'
                    '    public function encode(array $payload, int $ttl = 3600): string {\n'
                    '        $header = base64_encode(json_encode([\'typ\' => \'JWT\', \'alg\' => \'HS256\']));\n'
                    '        $payload[\'exp\'] = time() + $ttl;\n'
                    '        $body = base64_encode(json_encode($payload));\n'
                    '        $signature = hash_hmac(\'sha256\', "{$header}.{$body}", $this->secretKey, true);\n'
                    '        return "{$header}.{$body}." . base64_encode($signature);\n'
                    '    }\n'
                    '\n'
                    '    public function decode(string $token): ?array {\n'
                    '        $parts = explode(\'.\', $token);\n'
                    '        if (count($parts) !== 3) return null;\n'
                    '        [$header, $body, $sig] = $parts;\n'
                    '        $expected = base64_encode(hash_hmac(\'sha256\', "{$header}.{$body}", $this->secretKey, true));\n'
                    '        if (!hash_equals($expected, $sig)) return null;\n'
                    '        $payload = json_decode(base64_decode($body), true);\n'
                    '        if (($payload[\'exp\'] ?? 0) < time()) return null;\n'
                    '        return $payload;\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
    },
    'csharp': {
        'easy': [
            {
                'title': 'Record with positional params',
                'code': (
                    'public record UserSummary(\n'
                    '    int Id,\n'
                    '    string Username,\n'
                    '    string Email,\n'
                    '    DateTime CreatedAt\n'
                    ');\n'
                    '\n'
                    'var user = new UserSummary(1, "neo", "neo@matrix.io", DateTime.UtcNow);\n'
                    'Console.WriteLine($"User: {user.Username} ({user.Email})");\n'
                ),
            },
            {
                'title': 'Generic repository interface',
                'code': (
                    'public interface IRepository<T> where T : class\n'
                    '{\n'
                    '    Task<T?> GetByIdAsync(int id, CancellationToken ct = default);\n'
                    '    Task<IReadOnlyList<T>> ListAllAsync(CancellationToken ct = default);\n'
                    '    Task<T> AddAsync(T entity, CancellationToken ct = default);\n'
                    '    Task DeleteAsync(T entity, CancellationToken ct = default);\n'
                    '}\n'
                ),
            },
            {
                'title': 'LINQ aggregation by initial',
                'code': (
                    'public static Dictionary<string, int> CountWordsByInitial(IEnumerable<string> words)\n'
                    '{\n'
                    '    return words\n'
                    '        .Where(w => !string.IsNullOrWhiteSpace(w))\n'
                    '        .GroupBy(w => char.ToUpperInvariant(w[0]).ToString())\n'
                    '        .ToDictionary(g => g.Key, g => g.Count());\n'
                    '}\n'
                ),
            },
            {
                'title': 'String truncation extension',
                'code': (
                    'public static class StringExtensions\n'
                    '{\n'
                    '    public static string Truncate(this string? text, int maxLength, string suffix = "...")\n'
                    '    {\n'
                    '        if (string.IsNullOrEmpty(text) || text.Length <= maxLength)\n'
                    '            return text ?? string.Empty;\n'
                    '\n'
                    '        return text[..(maxLength - suffix.Length)] + suffix;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Custom Result pattern struct',
                'code': (
                    'public readonly struct Result<T>\n'
                    '{\n'
                    '    public bool IsSuccess { get; }\n'
                    '    public T? Value { get; }\n'
                    '    public string? Error { get; }\n'
                    '\n'
                    '    public Result(T value) => (IsSuccess, Value, Error) = (true, value, null);\n'
                    '    public Result(string error) => (IsSuccess, Value, Error) = (false, default, error);\n'
                    '}\n'
                ),
            },
        ],
        'medium': [
            {
                'title': 'ASP.NET Core Minimal API',
                'code': (
                    'var builder = WebApplication.CreateBuilder(args);\n'
                    'builder.Services.AddSingleton<ITypingService, TypingService>();\n'
                    '\n'
                    'var app = builder.Build();\n'
                    '\n'
                    'app.MapGet("/api/snippets/{id:int}", async (int id, ITypingService service) =>\n'
                    '{\n'
                    '    var snippet = await service.GetSnippetByIdAsync(id);\n'
                    '    return snippet is not null \n'
                    '        ? Results.Ok(snippet) \n'
                    '        : Results.NotFound(new { message = $"Snippet {id} not found." });\n'
                    '});\n'
                    '\n'
                    'app.MapPost("/api/attempts", async (AttemptDto dto, ITypingService service) =>\n'
                    '{\n'
                    '    var result = await service.RecordAttemptAsync(dto);\n'
                    '    return Results.Created($"/api/attempts/{result.Id}", result);\n'
                    '});\n'
                    '\n'
                    'app.Run();\n'
                ),
            },
            {
                'title': 'MemoryCache wrapper service',
                'code': (
                    'public class CacheService : ICacheService\n'
                    '{\n'
                    '    private readonly IMemoryCache _memoryCache;\n'
                    '    private readonly TimeSpan _defaultTtl = TimeSpan.FromMinutes(10);\n'
                    '\n'
                    '    public CacheService(IMemoryCache memoryCache) => _memoryCache = memoryCache;\n'
                    '\n'
                    '    public async Task<T> GetOrCreateAsync<T>(string key, Func<Task<T>> factory, TimeSpan? ttl = null)\n'
                    '    {\n'
                    '        if (_memoryCache.TryGetValue(key, out T? cachedItem) && cachedItem is not null)\n'
                    '            return cachedItem;\n'
                    '\n'
                    '        var newItem = await factory();\n'
                    '        _memoryCache.Set(key, newItem, ttl ?? _defaultTtl);\n'
                    '        return newItem;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'MediatR logging pipeline',
                'code': (
                    'public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>\n'
                    '    where TRequest : notnull\n'
                    '{\n'
                    '    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;\n'
                    '\n'
                    '    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger) => _logger = logger;\n'
                    '\n'
                    '    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken ct)\n'
                    '    {\n'
                    '        var requestName = typeof(TRequest).Name;\n'
                    '        _logger.LogInformation("Handling {RequestName}", requestName);\n'
                    '\n'
                    '        var stopwatch = Stopwatch.StartNew();\n'
                    '        var response = await next();\n'
                    '        stopwatch.Stop();\n'
                    '\n'
                    '        _logger.LogInformation("Handled {RequestName} in {ElapsedMs}ms", requestName, stopwatch.ElapsedMilliseconds);\n'
                    '        return response;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Generic binary search',
                'code': (
                    'public static class SearchAlgorithms\n'
                    '{\n'
                    '    public static int BinarySearch<T>(IReadOnlyList<T> list, T target) where T : IComparable<T>\n'
                    '    {\n'
                    '        int left = 0;\n'
                    '        int right = list.Count - 1;\n'
                    '\n'
                    '        while (left <= right)\n'
                    '        {\n'
                    '            int mid = left + (right - left) / 2;\n'
                    '            int comparison = list[mid].CompareTo(target);\n'
                    '\n'
                    '            if (comparison == 0) return mid;\n'
                    '            if (comparison < 0) left = mid + 1;\n'
                    '            else right = mid - 1;\n'
                    '        }\n'
                    '\n'
                    '        return -1;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Periodic background service',
                'code': (
                    'public class MetricsReporterService : BackgroundService\n'
                    '{\n'
                    '    private readonly ILogger<MetricsReporterService> _logger;\n'
                    '    private readonly PeriodicTimer _timer = new(TimeSpan.FromSeconds(30));\n'
                    '\n'
                    '    public MetricsReporterService(ILogger<MetricsReporterService> logger) => _logger = logger;\n'
                    '\n'
                    '    protected override async Task ExecuteAsync(CancellationToken stoppingToken)\n'
                    '    {\n'
                    '        while (await _timer.WaitForNextTickAsync(stoppingToken))\n'
                    '        {\n'
                    '            var memoryUsage = GC.GetTotalMemory(forceFullCollection: false) / 1024 / 1024;\n'
                    '            _logger.LogInformation("GC Memory allocated: {MemoryMb} MB", memoryUsage);\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
        ],
        'hard': [
            {
                'title': 'Thread-safe ObjectPool',
                'code': (
                    'public class ObjectPool<T> where T : class\n'
                    '{\n'
                    '    private readonly ConcurrentBag<T> _objects = new();\n'
                    '    private readonly Func<T> _generator;\n'
                    '    private readonly Action<T>? _reset;\n'
                    '    private readonly int _maxCapacity;\n'
                    '\n'
                    '    public ObjectPool(Func<T> generator, Action<T>? reset = null, int maxCapacity = 32)\n'
                    '    {\n'
                    '        _generator = generator ?? throw new ArgumentNullException(nameof(generator));\n'
                    '        _reset = reset;\n'
                    '        _maxCapacity = maxCapacity;\n'
                    '    }\n'
                    '\n'
                    '    public T Rent()\n'
                    '    {\n'
                    '        if (_objects.TryTake(out var item))\n'
                    '            return item;\n'
                    '\n'
                    '        return _generator();\n'
                    '    }\n'
                    '\n'
                    '    public void Return(T item)\n'
                    '    {\n'
                    '        _reset?.Invoke(item);\n'
                    '        if (_objects.Count < _maxCapacity)\n'
                    '        {\n'
                    '            _objects.Add(item);\n'
                    '        }\n'
                    '        else if (item is IDisposable disposable)\n'
                    '        {\n'
                    '            disposable.Dispose();\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Middleware pipeline builder',
                'code': (
                    'public delegate Task PipelineDelegate(HttpContext context);\n'
                    '\n'
                    'public class PipelineBuilder\n'
                    '{\n'
                    '    private readonly List<Func<PipelineDelegate, PipelineDelegate>> _components = new();\n'
                    '\n'
                    '    public PipelineBuilder Use(Func<HttpContext, Func<Task>, Task> middleware)\n'
                    '    {\n'
                    '        return Use(next => context => middleware(context, () => next(context)));\n'
                    '    }\n'
                    '\n'
                    '    public PipelineBuilder Use(Func<PipelineDelegate, PipelineDelegate> middleware)\n'
                    '    {\n'
                    '        _components.Add(middleware);\n'
                    '        return this;\n'
                    '    }\n'
                    '\n'
                    '    public PipelineDelegate Build()\n'
                    '    {\n'
                    '        PipelineDelegate app = _ => Task.CompletedTask;\n'
                    '        for (int i = _components.Count - 1; i >= 0; i--)\n'
                    '        {\n'
                    '            app = _components[i](app);\n'
                    '        }\n'
                    '        return app;\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Concurrent Event Aggregator',
                'code': (
                    'public class EventAggregator : IEventAggregator\n'
                    '{\n'
                    '    private readonly ConcurrentDictionary<Type, List<object>> _subscriptions = new();\n'
                    '\n'
                    '    public void Subscribe<TEvent>(Action<TEvent> handler)\n'
                    '    {\n'
                    '        var type = typeof(TEvent);\n'
                    '        _subscriptions.AddOrUpdate(\n'
                    '            type,\n'
                    '            _ => new List<object> { handler },\n'
                    '            (_, list) => { lock (list) { list.Add(handler); } return list; }\n'
                    '        );\n'
                    '    }\n'
                    '\n'
                    '    public void Publish<TEvent>(TEvent eventMessage)\n'
                    '    {\n'
                    '        var type = typeof(TEvent);\n'
                    '        if (!_subscriptions.TryGetValue(type, out var list)) return;\n'
                    '\n'
                    '        List<object> snapshot;\n'
                    '        lock (list) { snapshot = new List<object>(list); }\n'
                    '\n'
                    '        foreach (var handler in snapshot)\n'
                    '        {\n'
                    '            if (handler is Action<TEvent> action)\n'
                    '            {\n'
                    '                action(eventMessage);\n'
                    '            }\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Exponential retry with jitter',
                'code': (
                    'public static class RetryPolicy\n'
                    '{\n'
                    '    public static async Task<T> ExecuteWithRetryAsync<T>(\n'
                    '        Func<CancellationToken, Task<T>> operation,\n'
                    '        int maxRetries = 3,\n'
                    '        TimeSpan initialDelay = default,\n'
                    '        CancellationToken ct = default)\n'
                    '    {\n'
                    '        if (initialDelay == default) initialDelay = TimeSpan.FromMilliseconds(200);\n'
                    '        var random = new Random();\n'
                    '\n'
                    '        for (int attempt = 1; ; attempt++)\n'
                    '        {\n'
                    '            try\n'
                    '            {\n'
                    '                return await operation(ct);\n'
                    '            }\n'
                    '            catch (Exception) when (attempt < maxRetries && !ct.IsCancellationRequested)\n'
                    '            {\n'
                    '                var delayMs = (int)(initialDelay.TotalMilliseconds * Math.Pow(2, attempt - 1));\n'
                    '                var jitter = random.Next(-delayMs / 4, delayMs / 4);\n'
                    '                await Task.Delay(Math.Max(50, delayMs + jitter), ct);\n'
                    '            }\n'
                    '        }\n'
                    '    }\n'
                    '}\n'
                ),
            },
            {
                'title': 'Polymorphic JSON converter',
                'code': (
                    'public class ShapeJsonConverter : JsonConverter<Shape>\n'
                    '{\n'
                    '    public override Shape? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)\n'
                    '    {\n'
                    '        using var jsonDoc = JsonDocument.ParseValue(ref reader);\n'
                    '        var root = jsonDoc.RootElement;\n'
                    '        var typeProperty = root.GetProperty("type").GetString();\n'
                    '\n'
                    '        return typeProperty switch\n'
                    '        {\n'
                    '            "circle" => JsonSerializer.Deserialize<Circle>(root.GetRawText(), options),\n'
                    '            "rectangle" => JsonSerializer.Deserialize<Rectangle>(root.GetRawText(), options),\n'
                    '            _ => throw new JsonException($"Unknown shape type: \'{typeProperty}\'")\n'
                    '        };\n'
                    '    }\n'
                    '\n'
                    '    public override void Write(Utf8JsonWriter writer, Shape value, JsonSerializerOptions options)\n'
                    '    {\n'
                    '        JsonSerializer.Serialize(writer, (object)value, value.GetType(), options);\n'
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

