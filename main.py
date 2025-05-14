from flet import Page, PagePlatform, app
from views.Router import Router
from db.flet_pyrebase import PyrebaseWrapper

def main(page: Page):
    # Settings for the page
    page.title = "App Multirobot"
    # page.platform = PagePlatform.LINUX
    myPyrebase = PyrebaseWrapper(page)
    myRouter = Router(page, myPyrebase)
    page.on_route_change = myRouter.route_change
    page.add(myRouter.body)
    page.go("/")


app(main, assets_dir="assets")
