from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def build(ctx):
    ctx.run("mkdir src/data/saves")

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src")
    ctx.run("coverage report -m")
    ctx.run("coverage html")

@task
def lint(ctx):
    ctx.run("pylint src")

# A temporary task for GUI testing
@task
def test_gui(ctx):
    ctx.run("python3 src/main.py")
