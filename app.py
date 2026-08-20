import requests
import streamlit as st
import os

# =========================================================
# CONFIG
# =========================================================

API_BASE = os.getenv(
    "API_BASE",
    "https://movie-recommendation-api-jeqy.onrender.com"
)

TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP = "https://image.tmdb.org/t/p/original"

st.set_page_config(
    page_title="Menu",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SESSION STATE
# =========================================================

if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

if "search_text" not in st.session_state:
    st.session_state.search_text = ""


# =========================================================
# STREAMLIT STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */

    .block-container {
        max-width: 1400px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        padding-left: 4%;
        padding-right: 4%;
    }

    /* Buttons */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
    }

    /* Images */

    img {
        border-radius: 12px;
    }

    /* Search input */

    .stTextInput input {
        border-radius: 12px;
        min-height: 45px;
    }

    /* Selectbox */

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
    }

    /* Hero */

    .hero-title {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        line-height: 1.1;
    }

    .hero-text {
        font-size: clamp(0.95rem, 2vw, 1.1rem);
        opacity: 0.75;
        max-width: 800px;
        line-height: 1.6;
    }

    /* Movie title */

    .movie-name {
        font-size: 0.95rem;
        font-weight: 700;
        line-height: 1.3;
        margin-top: 8px;
        min-height: 42px;
    }

    /* Fixed movie title height */

    .movie-card-title {
        height: 45px;
        overflow: hidden;
        display: flex;
        align-items: flex-start;
        font-size: 0.95rem;
        font-weight: 700;
        line-height: 1.3;
        margin-top: 8px;
    }

    /* Small text */

    .muted {
        opacity: 0.65;
        font-size: 0.85rem;
    }

    /* Detail text */

    .overview-text {
        font-size: 1rem;
        line-height: 1.7;
    }

    /* Mobile */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 4%;
            padding-right: 4%;
            padding-top: 0.8rem;
        }

        .hero-title {
            font-size: 2rem;
        }

        .hero-text {
            font-size: 0.9rem;
        }

        .movie-name {
            font-size: 0.85rem;
            min-height: 38px;
        }

        .movie-card-title {
            height: 40px;
            font-size: 0.85rem;
        }

        .stButton > button {
            min-height: 40px;
            font-size: 0.85rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# NAVIGATION
# =========================================================

def goto_home():

    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None

    st.query_params["view"] = "home"

    if "id" in st.query_params:
        del st.query_params["id"]

    st.rerun()


def goto_details(tmdb_id):

    if not tmdb_id:
        return

    try:
        tmdb_id = int(tmdb_id)
    except (ValueError, TypeError):
        return

    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = tmdb_id

    st.query_params["view"] = "details"
    st.query_params["id"] = str(tmdb_id)

    st.rerun()


# =========================================================
# READ URL
# =========================================================

query_view = st.query_params.get("view")
query_id = st.query_params.get("id")

if query_view in ("home", "details"):
    st.session_state.view = query_view

if query_id:

    try:
        st.session_state.selected_tmdb_id = int(query_id)
        st.session_state.view = "details"
    except (ValueError, TypeError):
        pass


# =========================================================
# API HELPER
# =========================================================

@st.cache_data(ttl=30)
def api_get_json(path, params=None):

    try:

        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=20,
        )

        if response.status_code >= 400:

            return None, (
                f"HTTP {response.status_code}: "
                f"{response.text[:250]}"
            )

        try:
            return response.json(), None

        except ValueError:

            return None, "Backend returned invalid JSON."

    except requests.exceptions.ConnectionError:

        return None, (
            "Backend not connected. "
            "Please start FastAPI on port 8000."
        )

    except requests.exceptions.Timeout:

        return None, (
            "Backend took too long to respond."
        )

    except requests.exceptions.RequestException as error:

        return None, str(error)

    except Exception as error:

        return None, str(error)


# =========================================================
# IMAGE HELPERS
# =========================================================

def build_image_url(
    url=None,
    path=None,
    base_url=TMDB_IMG,
):

    if url:

        url = str(url).strip()

        if url.startswith("http"):
            return url

        if url.startswith("/"):
            return f"{base_url}{url}"

        return f"{base_url}/{url}"

    if path:

        path = str(path).strip()

        if path.startswith("http"):
            return path

        if path.startswith("/"):
            return f"{base_url}{path}"

        return f"{base_url}/{path}"

    return None


def get_poster_url(movie):

    if not isinstance(movie, dict):
        return None

    return build_image_url(
        movie.get("poster_url"),
        movie.get("poster_path"),
        TMDB_IMG,
    )


def get_backdrop_url(movie):

    if not isinstance(movie, dict):
        return None

    return build_image_url(
        movie.get("backdrop_url"),
        movie.get("backdrop_path"),
        TMDB_BACKDROP,
    )


# =========================================================
# MOVIE CARD GRID
# =========================================================

def poster_grid(
    cards,
    cols=6,
    key_prefix="movie",
):

    if not cards:

        st.info(
            "No movies available."
        )

        return

    cards = [
        movie
        for movie in cards
        if isinstance(movie, dict)
    ]

    if not cards:

        st.info(
            "No valid movie data received."
        )

        return

    rows = (
        len(cards) + cols - 1
    ) // cols

    index = 0

    for row in range(rows):

        columns = st.columns(
            cols,
            gap="small",
        )

        for column_number in range(cols):

            if index >= len(cards):
                break

            movie = cards[index]

            movie_index = index

            index += 1

            tmdb_id = (
                movie.get("tmdb_id")
                or movie.get("id")
            )

            title = (
                movie.get("title")
                or movie.get("name")
                or "Untitled"
            )

            release_date = (
                movie.get("release_date")
                or movie.get("first_air_date")
                or ""
            )

            poster = get_poster_url(movie)

            with columns[column_number]:

                # -----------------------------------------
                # POSTER
                # -----------------------------------------

                if poster:

                    st.image(
                        poster,
                        width="stretch",
                    )

                else:

                    st.info(
                        "🖼️ No poster"
                    )

                # -----------------------------------------
                # TITLE
                # -----------------------------------------

                st.markdown(
                    f"<div class='movie-card-title'>{title}</div>",
                    unsafe_allow_html=True,
                )

                # -----------------------------------------
                # YEAR
                # -----------------------------------------

                if release_date:

                    st.markdown(
                        f"<div style='height:24px;'>📅 {str(release_date)[:4]}</div>",
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        "<div style='height:24px;'></div>",
                        unsafe_allow_html=True,
                    )

                # -----------------------------------------
                # OPEN
                # -----------------------------------------

                if tmdb_id:

                    if st.button(
                        "🎬 Open",
                        key=(
                            f"{key_prefix}_"
                            f"{row}_"
                            f"{column_number}_"
                            f"{movie_index}_"
                            f"{tmdb_id}"
                        ),
                    ):

                        goto_details(
                            tmdb_id
                        )


# =========================================================
# SEARCH PARSER
# =========================================================

def parse_tmdb_search_to_cards(
    data,
    keyword,
    limit=24,
):

    raw_items = []

    keyword = (
        keyword.strip().lower()
    )

    # -----------------------------------------------------
    # API RETURNS {"results": [...]}
    # -----------------------------------------------------

    if (
        isinstance(data, dict)
        and "results" in data
    ):

        results = data.get(
            "results"
        ) or []

        for movie in results:

            if not isinstance(movie, dict):
                continue

            title = (
                movie.get("title")
                or movie.get("name")
                or ""
            ).strip()

            tmdb_id = (
                movie.get("id")
                or movie.get("tmdb_id")
            )

            if not title or not tmdb_id:
                continue

            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": movie.get(
                        "poster_url"
                    ),
                    "poster_path": movie.get(
                        "poster_path"
                    ),
                    "release_date": movie.get(
                        "release_date"
                    )
                    or movie.get(
                        "first_air_date"
                    )
                    or "",
                }
            )

    # -----------------------------------------------------
    # API RETURNS [...]
    # -----------------------------------------------------

    elif isinstance(data, list):

        for movie in data:

            if not isinstance(movie, dict):
                continue

            tmdb_id = (
                movie.get("tmdb_id")
                or movie.get("id")
            )

            title = (
                movie.get("title")
                or movie.get("name")
                or ""
            ).strip()

            if not title or not tmdb_id:
                continue

            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": movie.get(
                        "poster_url"
                    ),
                    "poster_path": movie.get(
                        "poster_path"
                    ),
                    "release_date": movie.get(
                        "release_date"
                    )
                    or "",
                }
            )

    else:

        return [], []

    # -----------------------------------------------------
    # KEYWORD MATCH
    # -----------------------------------------------------

    matched = [
        movie
        for movie in raw_items
        if keyword in movie["title"].lower()
    ]

    final_items = (
        matched
        if matched
        else raw_items
    )

    # -----------------------------------------------------
    # SUGGESTIONS
    # -----------------------------------------------------

    suggestions = []

    for movie in final_items[:10]:

        release_date = (
            movie.get(
                "release_date"
            )
            or ""
        )

        year = str(
            release_date
        )[:4]

        if year:

            label = (
                f"{movie['title']} "
                f"({year})"
            )

        else:

            label = movie["title"]

        suggestions.append(
            (
                label,
                movie["tmdb_id"],
            )
        )

    # -----------------------------------------------------
    # CARDS
    # -----------------------------------------------------

    cards = final_items[:limit]

    return suggestions, cards


# =========================================================
# TF-IDF
# =========================================================

def to_cards_from_tfidf_items(items):

    cards = []

    for item in items or []:

        if not isinstance(item, dict):
            continue

        tmdb = (
            item.get("tmdb")
            or {}
        )

        if not isinstance(tmdb, dict):
            continue

        tmdb_id = (
            tmdb.get("tmdb_id")
            or tmdb.get("id")
        )

        if not tmdb_id:
            continue

        cards.append(
            {
                "tmdb_id": tmdb_id,
                "title": (
                    tmdb.get("title")
                    or item.get("title")
                    or "Untitled"
                ),
                "poster_url": tmdb.get(
                    "poster_url"
                ),
                "poster_path": tmdb.get(
                    "poster_path"
                ),
                "release_date": tmdb.get(
                    "release_date"
                ),
            }
        )

    return cards


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title(
        "🎬 Menu"
    )

    st.caption(
        "Discover movies you will love."
    )

    st.divider()

    if st.button(
        "🏠 Home",
    ):

        goto_home()

    st.divider()

    st.subheader(
        "Home Feed"
    )

    home_category = st.selectbox(
        "Choose category",
        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming",
        ],
        index=0,
    )

    grid_cols = st.slider(
        "Movies per row",
        2,
        8,
        6,
    )

    st.divider()

    st.caption(
        "TMDB • FastAPI • Streamlit"
    )


# =========================================================
# HOME
# =========================================================

if st.session_state.view == "home":

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.title(
        "🎬 Movie Recommender"
    )

    st.write(
        "Search movies, explore detailed information, "
        "and discover similar movies using intelligent "
        "recommendations."
    )

    st.divider()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    st.subheader(
        "🔎 Search Movies"
    )

    typed = st.text_input(
        "Movie title",
        placeholder=(
            "Avenger, Batman, "
            "Spider man ..."
        ),
        label_visibility="collapsed",
    )

    # -----------------------------------------------------
    # SEARCH RESULTS
    # -----------------------------------------------------

    if typed.strip():

        if len(typed.strip()) < 2:

            st.info(
                "Type at least 2 characters."
            )

        else:

            with st.spinner(
                "Searching movies..."
            ):

                data, error = api_get_json(
                    "/tmdb/search",
                    params={
                        "query": typed.strip()
                    },
                )

            if error:

                st.error(
                    f"Search failed: {error}"
                )

            else:

                suggestions, cards = (
                    parse_tmdb_search_to_cards(
                        data,
                        typed,
                        24,
                    )
                )

                if suggestions:

                    labels = [
                        "-- Select a movie --"
                    ]

                    labels.extend(
                        [
                            item[0]
                            for item in suggestions
                        ]
                    )

                    selected = st.selectbox(
                        "🎯 Movie suggestions",
                        labels,
                    )

                    if (
                        selected
                        != "-- Select a movie --"
                    ):

                        label_to_id = {
                            item[0]: item[1]
                            for item in suggestions
                        }

                        movie_id = (
                            label_to_id.get(
                                selected
                            )
                        )

                        if movie_id:

                            goto_details(
                                movie_id
                            )

                else:

                    st.warning(
                        "No movies found."
                    )

                st.subheader(
                    "🔎 Search Results"
                )

                poster_grid(
                    cards,
                    cols=grid_cols,
                    key_prefix="search",
                )

    # -----------------------------------------------------
    # HOME FEED
    # -----------------------------------------------------

    else:

        st.subheader(
            "🔥 "
            + home_category.replace(
                "_",
                " ",
            ).title()
        )

        with st.spinner(
            "Loading movies..."
        ):

            home_cards, error = api_get_json(
                "/home",
                params={
                    "category": home_category,
                    "limit": 24,
                },
            )

        if error:

            st.error(
                f"Home feed failed: {error}"
            )

        elif not home_cards:

            st.warning(
                "No movies available."
            )

        else:

            poster_grid(
                home_cards,
                cols=grid_cols,
                key_prefix="home",
            )


# =========================================================
# DETAILS
# =========================================================

elif st.session_state.view == "details":

    tmdb_id = (
        st.session_state.selected_tmdb_id
    )

    if not tmdb_id:

        st.warning(
            "No movie selected."
        )

        if st.button(
            "← Back to Home",
        ):

            goto_home()

        st.stop()

    # -----------------------------------------------------
    # TOP BAR
    # -----------------------------------------------------

    col1, col2 = st.columns(
        [4, 1]
    )

    with col1:

        st.title(
            "📄 Movie Details"
        )

    with col2:

        if st.button(
            "← Home",
        ):

            goto_home()

    # -----------------------------------------------------
    # GET MOVIE
    # -----------------------------------------------------

    with st.spinner(
        "Loading movie..."
    ):

        data, error = api_get_json(
            f"/movie/id/{tmdb_id}"
        )

    if error or not data:

        st.error(
            f"Could not load movie: "
            f"{error or 'Unknown error'}"
        )

        st.stop()

    title = (
        data.get("title")
        or "Untitled Movie"
    )

    poster = get_poster_url(
        data
    )

    backdrop = get_backdrop_url(
        data
    )

    release_date = (
        data.get("release_date")
        or "-"
    )

    overview = (
        data.get("overview")
        or "No overview available."
    )

    # -----------------------------------------------------
    # BACKDROP
    # -----------------------------------------------------

    if backdrop:

        st.image(
            backdrop,
            width="stretch",
        )

    # -----------------------------------------------------
    # DETAILS
    # -----------------------------------------------------

    poster_col, details_col = st.columns(
        [1, 2],
        gap="large",
    )

    with poster_col:

        if poster:

            st.image(
                poster,
                width="stretch",
            )

        else:

            st.info(
                "🖼️ Poster unavailable"
            )

    with details_col:

        st.header(
            title
        )

        st.write(
            f"📅 **Release:** {release_date}"
        )

        genres = data.get(
            "genres",
            [],
        )

        genre_names = []

        if isinstance(
            genres,
            list,
        ):

            for genre in genres:

                if isinstance(
                    genre,
                    dict,
                ):

                    name = genre.get(
                        "name"
                    )

                    if name:
                        genre_names.append(
                            name
                        )

        if genre_names:

            st.write(
                "🎭 **Genres:** "
                + ", ".join(
                    genre_names
                )
            )

        st.divider()

        st.subheader(
            "📝 Overview"
        )

        st.write(
            overview
        )

    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    st.divider()

    st.title(
        "🤖 Recommended Movies"
    )

    with st.spinner(
        "Finding similar movies..."
    ):

        bundle, error = api_get_json(
            "/movie/search",
            params={
                "query": title,
                "tfidf_top_n": 12,
                "genre_limit": 12,
            },
        )

    if not error and bundle:

        st.subheader(
            "🔎 Similar Movies"
        )

        tfidf_cards = (
            to_cards_from_tfidf_items(
                bundle.get(
                    "tfidf_recommendations",
                    [],
                )
            )
        )

        poster_grid(
            tfidf_cards,
            cols=grid_cols,
            key_prefix="tfidf",
        )

        st.subheader(
            "🎭 More Like This"
        )

        genre_cards = bundle.get(
            "genre_recommendations",
            [],
        )

        poster_grid(
            genre_cards,
            cols=grid_cols,
            key_prefix="genre",
        )

    else:

        st.info(
            "Trying genre recommendations..."
        )

        genre_only, genre_error = api_get_json(
            "/recommend/genre",
            params={
                "tmdb_id": tmdb_id,
                "limit": 18,
            },
        )

        if not genre_error and genre_only:

            poster_grid(
                genre_only,
                cols=grid_cols,
                key_prefix="genre_fallback",
            )

        else:

            st.warning(
                "No recommendations available right now."
            )