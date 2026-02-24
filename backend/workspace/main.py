import sys

def greet(name):
    print(f'Hello, {name}!')


def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'World'
    greet(name)


if __name__ == '__main__':
    main()