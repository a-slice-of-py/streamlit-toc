from dataclasses import dataclass
from types import ModuleType
from typing import Callable, Iterable, Optional, Union

import streamlit as st
from streamlit_option_menu import option_menu as st_menu
from contextlib import nullcontext


@dataclass
class Page:
    uid: str
    title: str
    icon: str
    contents: Union[ModuleType, Callable]
    index: int
    show_to: Optional[list] = None

class ToC:

    def __init__(self,
                pages: Iterable[Page]
                ) -> None:
        """Init class.

        Args:
            pages (Iterable[Page]): available pages.
        """
        self.pages = sorted(
            filter(
                lambda x: x.show_to is None or st.session_state.get('username') in x.show_to,
                pages
            ),
            key=lambda x: x.index
        )

    def get_pages(self, by: str) -> list:
        """Get pages by attribute.

        Args:
            by (str): attribute name.

        Returns:
            Pages attributes.
        """
        return list(getattr(page, by) for page in self.pages)

    def _get_page_by_title(self, title: str) -> Page:
        """Get page by title.

        Args:
            title (str): page title.

        Returns:
            Page.
        """
        return self.pages[self.get_pages(by='title').index(title)]

    def load_page(self, title: str, show_title: bool = False) -> None:
        """Load page contents.

        Args:
            title (str): page title.
        """
        if show_title:
            st.title(title)
        contents = self._get_page_by_title(title).contents
        if isinstance(contents, Callable):
            contents()
        elif isinstance(contents, ModuleType):
            # SEE: assume that contents module define
            # a load() function
            contents.load()


def display_toc(toc: ToC, 
                in_sidebar: bool, 
                menu_title: Optional[str] = None
                ) -> str:
    context = st.sidebar if in_sidebar else nullcontext()
    orientation = 'vertical' if in_sidebar else 'horizontal'
    with context:
        page_title = st_menu(
            menu_title=menu_title,
            options=toc.get_pages(by='title'),
            orientation=orientation,
            icons=toc.get_pages(by='icon')
        )
    return page_title


def main() -> None:

    def page_1():
        st.markdown("## Hello from ToC! 👋")
        st.markdown('''
        I am a possible solution to manage multi-page Streamlit apps using streamlit-option-menu! 🎉🎉🎉
        <br>First of all, I define a `Page` dataclass:
        ''', 
        unsafe_allow_html=True
        )
        '''
        ```python
        @dataclass
        class Page:
            uid: str
            title: str
            icon: str
            contents: Union[ModuleType, Callable]
            index: int
            show_to: Optional[list] = None
        ```
        '''
        st.markdown('''
        where you can set a handy page `uid`, a `title` to be displayed as page and the `icon` name.

        Moreover, you can pass a function (or a module which defines a `load()` function) in `contents` to define complex page contents as well as choose an `index` to have more control on the order of pages in the menu.

        Finally, you can restrict user access to the page by whitelisting only certain usernames in `show_to` (works like a charm in combo with [authentication](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso)!)
        
        ### 👉 Use the menu to proceed to Page 2!
        ''',
        unsafe_allow_html=True
        )        


    def page_2():
        st.markdown("Since `Page` has been defined in Page 1, we can finally define `ToC`!")
        
        with st.expander('Source code', expanded=False):        
            '''
            ```python
            class ToC:

                def __init__(self,
                            pages: Iterable[Page]
                            ) -> None:
                    """Init class.

                    Args:
                        pages (Iterable[Page]): available pages.
                    """
                    self.pages = sorted(
                        filter(
                            lambda x: (
                                x.show_to is None 
                                or st.session_state.get('username') in x.show_to
                                ),
                            pages
                        ),
                        key=lambda x: x.index
                    )

                def get_pages(self, by: str) -> list:
                    """Get pages by attribute.

                    Args:
                        by (str): attribute name.

                    Returns:
                        Pages attributes.
                    """
                    return list(getattr(page, by) for page in self.pages)

                def _get_page_by_title(self, title: str) -> Page:
                    """Get page by title.

                    Args:
                        title (str): page title.

                    Returns:
                        Page.
                    """
                    return self.pages[self.get_pages(by='title').index(title)]

                def load_page(self, title: str, show_title: bool = False) -> None:
                    """Load page contents.

                    Args:
                        title (str): page title.
                    """
                    if show_title:
                        st.title(title)
                    contents = self._get_page_by_title(title).contents
                    if isinstance(contents, Callable):
                        contents()
                    elif isinstance(contents, ModuleType):
                        # SEE: assume that contents module define
                        # a load() function
                        contents.load()
            ```
            '''
        st.markdown('''
        ToC acts just like a simple collections of Pages with some handy accessors methods.

        ```python
        toc = ToC([Page(...), Page(...)])
        ```

        Once we have listed our pages and wrapped them into a ToC, we just have to rely on `display_toc()` utility:
        '''
        )
        with st.expander('Source code', expanded=False):
            '''
            ```python
            def display_toc(toc: ToC, 
                            in_sidebar: bool, 
                            menu_title: Optional[str] = None
                            ) -> str:
                context = st.sidebar if in_sidebar else nullcontext()
                orientation = 'vertical' if in_sidebar else 'horizontal'
                with context:
                    page_title = st_menu(
                        menu_title=menu_title,
                        options=toc.get_pages(by='title'),
                        orientation=orientation,
                        icons=toc.get_pages(by='icon')
                    )
                return page_title
            ```
            '''
        st.markdown('''
        and then ask ToC to load the chosen page!
        ```python
        page_title = display_toc(toc, in_sidebar=in_sidebar, menu_title=menu_title)
        toc.load_page(title=page_title, show_title=show_title)
        ```

        ### Ok, that's all... or not? 😏 
        _Maybe_ some <font style="color:red">super secret and never-seen-before username</font> can access to some secret page..?!
        ''', 
        unsafe_allow_html=True)

    def page_3():
        st.markdown("## Awesome! You found the secret page 🕶️")

        st.image(image='https://pbs.twimg.com/media/Em03ZTtWEAgy8sR.jpg')

    toc = ToC([
        Page(
            uid='page2',
            title='Page 2',
            icon='hand-index-thumb',
            contents=page_2,
            index=1
        ),
        Page(
            uid='page3',
            title='Secret page',
            icon='arrow-up-circle',
            contents=page_3,
            index=2,
            show_to=['admin']
        ),
        Page(
            uid='page1',
            title='Page 1',
            icon='person-square',
            contents=page_1,
            index=0
        ),
    ])
    with st.sidebar:
        username = st.text_input(label='Username', value='user', key='username')
        menu_title = st.text_input(label='Menu title (optional)')
        left, right = st.columns(2)
        with left:
            in_sidebar = st.checkbox(label='Show menu in sidebar', value=True)
        with right:
            show_title = st.checkbox(label='Show page title', value=True)
    page_title = display_toc(toc, in_sidebar=in_sidebar, menu_title=menu_title)
    toc.load_page(title=page_title, show_title=show_title)


if __name__ == '__main__':
    st.set_page_config(
        page_title='ToC Demo',
        layout='centered',
        initial_sidebar_state='auto'
    )
    main()