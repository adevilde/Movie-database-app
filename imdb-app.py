import streamlit as st
import pandas as pd

from functions import create_connection_pool, get_db_connection, release_db_connection, query_db, is_number

# Streamlit application
def main():  

    # Use the connection from the session state
    conn = get_db_connection(st.session_state.connection_pool)

    st.markdown("<h1 style='text-align: center;'>Welcome to the Movie Database Application🎬🍿</h1>", unsafe_allow_html=True)
    st.write("This application allows you to search for movies, actors, and more.")

    # Display top-10 recent movies
    with open('./queries/recent_movies.sql', 'r') as file:
        recent_movies_query = file.read()

    recent_movies = query_db(conn, recent_movies_query, None)

    st.write("### Top-10 recent movies:")

    # Process the movies into a DataFrame
    movies_df = pd.DataFrame(recent_movies, columns=['ID', 'Title', 'Year', 'Rating'])

    # Format 'Rating' as a string with one decimal place
    movies_df['Rating'] = movies_df['Rating'].apply(lambda x: f"{float(x):.1f}")

    # Function to convert rating to stars with half stars
    def rating_to_stars(rating):
        full_stars = int(rating) // 2
        half_star = 1 if rating % 1 >= 0.5 else 0 
        return '★' * full_stars + '☆' * half_star

    # Apply the star conversion function to the 'Rating' column
    movies_df['Star Rating'] = movies_df['Rating'].astype(float).apply(rating_to_stars)

    # Display the DataFrame as a table in Streamlit
    st.table(movies_df)

# ---------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center;'>What are you looking for? 🤔</h2>", unsafe_allow_html=True)

    st.write("Select an option from the dropdown menu below to search for an actor, movie, or more.")

    # Menu options
    options = {
        "1": "Search for an actor",
        "2": "Search for a movie",
        "3": "Search for movies where two actors starred together",
        "4": "Search for movies of a genre",
        "5": "Search for movies of a production company",
    }

    choice = st.selectbox("Select an option", list(options.keys()), format_func=lambda x: options[x])

    if choice == "1":
        actor_input = st.text_input("Enter actor ID or name")
        if actor_input:
            if is_number(actor_input):

                # the input is an actor ID
                with open('./queries/actor_query_id.sql', 'r') as file:
                    actor_query_id = file.read()          
                actor_details = query_db(conn, actor_query_id, (actor_input,))

            else:
                # the input is an actor name
                with open('./queries/actor_query_name.sql', 'r') as file:
                    actor_query_name = file.read()
                actor_details = query_db(conn, actor_query_name, ('%'+actor_input+'%',))

            if actor_details:
                actor_df = pd.DataFrame(actor_details, columns=['Name', 'ID', 'Movies', 'Info Type', 'Info', 'AKA Name'])
                unique_actors = sorted(actor_df['Name'].unique())

                if len(unique_actors) > 1:
                    selected_actor_name = st.selectbox("There are different actors. Select one", unique_actors)
                    actor_df = actor_df[actor_df['Name'] == selected_actor_name]

                # Display the actor details
                st.write("### **General Information**")
                st.write(f"*ID:* {actor_df['ID'].values[0]}")
                
                names_str = "; ".join(actor_df['Name'].unique())
                st.write(f"*Name:* {names_str}")

                if None not in actor_df['AKA Name'].unique():
                    aka_names_str = "; ".join(actor_df['AKA Name'].unique())
                    st.write(f"*AKA Name:* {aka_names_str}")
                
                movies = actor_df['Movies'].unique()
                # TODO: if amongst the movies there are 'episode' (movie_type.kind = 7) then find 
                # the tv series name to print the tv series name and the episode number

                # Display the processed information
                st.write("### **Movies:**")
                if len(movies) > 1:
                    with st.expander("Click to expand"):
                        for movie in movies:
                            st.write(f"* {movie}")
                else:
                    st.write(f"{movies[0]}")
                st.write("")

                if None not in actor_df['Info Type'].unique():
                    info_types = sorted(actor_df['Info Type'].unique())
                    for info_type in info_types:
                        info = actor_df[actor_df['Info Type'] == info_type]
                        info = info['Info'].unique()
                        st.write(f"### **{info_type}:**")
                        if len(info) > 1:
                            with st.expander("Click to expand"):
                                for i in info:
                                    st.write(f"* {i}")
                        else:
                            st.write(f"{info[0]}")
                    st.write("")

            else:
                st.write("No actor/actress found with the given input.")


# ---------------------------------------------------------------------------------------------

    elif choice == "2":
        movie_input = st.text_input("Enter movie ID or name")
        if movie_input:

            if is_number(movie_input):
                # the input is a movie ID
                with open('./queries/movie_query_id.sql', 'r') as file:
                    movie_query_id = file.read()

                movie_details = query_db(conn, movie_query_id, (movie_input,))

            else:
                # the input is a movie name
                with open('./queries/movie_query_name.sql', 'r') as file:
                    movie_query_name = file.read()
                movie_details = query_db(conn, movie_query_name, ('%'+movie_input+'%',))

            if movie_details:
                movie_df = pd.DataFrame(movie_details, columns=['Title', 'ID', 'Info_type', 'Info', 'Kind', 'Year', 'Casting', 'Rating_info_type', 'Rating', 'Company'])
                unique_movies = sorted(movie_df['Title'].unique())

                if len(unique_movies) > 1:
                    selected_movie_name = st.selectbox("There are different movies. Select one", unique_movies)
                    movie_df = movie_df[movie_df['Title'] == selected_movie_name]

                # Display the movie details
                st.write("### **General Information**")
                st.write(f"*ID:* {movie_df['ID'].values[0]}")
                st.write(f"*Title:* **{movie_df['Title'].values[0]}**")

                companies = "; ".join(movie_df['Company'].unique())
                st.write(f"*Company:* {companies}")
                
                years = "; ".join(str(year) for year in movie_df['Year'].unique())
                st.write(f"*Year:* {years}")

                st.write(f"*Kind:* {movie_df['Kind'].values[0]}")

                rating_types = movie_df['Rating_info_type'].unique()

                for rating_type in rating_types:
                    rating = movie_df[movie_df['Rating_info_type'] == rating_type]['Rating']
                    if not rating.empty:
                        st.write(f"*{rating_type}:* {rating.values[0]}")

                Casting = movie_df['Casting'].unique()
                st.write(f"### **Casting:**")
                if len(Casting) > 1:
                    with st.expander("Click to expand"):
                        for casting_name in Casting:
                            st.write(f"* {casting_name}")
                else:
                    st.write(f"{Casting[0]}")
                st.write("")

                if None not in movie_df['Info_type'].unique():
                    info_types = sorted(movie_df['Info_type'].unique())
                    for info_type in info_types:
                        info = movie_df[movie_df['Info_type'] == info_type]
                        info = info['Info'].unique()
                        st.write(f"### **{info_type}:**")
                        if len(info) > 1:
                            with st.expander("Click to expand"):
                                for i in info:
                                    st.write(f"* {i}")
                        else:
                            st.write(f"{info[0]}")
                    st.write("")    

                if None not in movie_df['Rating_info_type'].unique():
                    rating_info_types = sorted(movie_df['Rating_info_type'].unique())
                    for rating_info_type in rating_info_types:
                        rating_info = movie_df[movie_df['Rating_info_type'] == rating_info_type]
                        rating_info = rating_info['Rating'].unique()
                        st.write(f"### **{rating_info_type}:**")
                        if len(rating_info) > 1:
                            with st.expander("Click to expand"):
                                for i in rating_info:
                                    st.write(f"* {i}")
                        else:
                            st.write(f"{rating_info[0]}")
                    st.write("")
                             
            else:
                st.write("No movie found with the given input.")
# ---------------------------------------------------------------------------------------------

    elif choice == "3":
        option = st.selectbox("Do you want to enter IDs or names?", ["IDs", "Names"])

        if option == "IDs":
            actor1_input = st.text_input("Enter the first actor ID")
            actor2_input = st.text_input("Enter the second actor ID")
        else:
            actor1_input = st.text_input("Enter the first actor name")
            actor2_input = st.text_input("Enter the second actor name")
        

        if actor1_input and actor2_input:

            if is_number(actor1_input) and is_number(actor2_input):
                with open('./queries/starred_movies_id.sql', 'r') as file:
                    starred_movies_id = file.read()
                starred_movies = query_db(conn, starred_movies_id, (actor1_input, actor2_input))
            else:
                with open('./queries/starred_movies_name.sql', 'r') as file:
                    starred_movies_name = file.read()
                starred_movies = query_db(conn, starred_movies_name, ('%'+actor1_input+'%', '%'+actor2_input+'%'))

            if starred_movies:
                starred_movie_df = pd.DataFrame(starred_movies, columns=['ID', 'Movie', 'Year', 'Rating', 'Actor1', 'Actor2'])
                unique_actors1 = sorted(starred_movie_df['Actor1'].unique())
                unique_actors2 = sorted(starred_movie_df['Actor2'].unique())

                if len(unique_actors1) > 1:
                    selected_actor1_name = st.selectbox("There are different actors. Select one", unique_actors1)
                    starred_movie_df = starred_movie_df[starred_movie_df['Actor1'] == selected_actor1_name]

                if len(unique_actors2) > 1:
                    selected_actor2_name = st.selectbox("There are different actors. Select one", unique_actors2)
                    starred_movie_df = starred_movie_df[starred_movie_df['Actor2'] == selected_actor2_name]

                if starred_movie_df.empty:
                    st.write("There is no movie where these actors starred together.")
                    return

                # Display the actors details
                st.write("### **General Information**")
                st.write(f"*Actor 1:* **{starred_movie_df['Actor1'].values[0]}**")
                st.write(f"*Actor 2:* **{starred_movie_df['Actor2'].values[0]}**")

                movies = starred_movie_df['Movie'].unique()
                st.write("### **Movies:**")
                if len(movies) > 1:
                    with st.expander("Click to expand"):
                        for movie in movies:
                            st.write(f"* {movie}")
                            st.write(f"*ID:* {starred_movie_df[starred_movie_df['Movie'] == movie]['ID'].values[0]}")
                            st.write(f"*Year:* {starred_movie_df[starred_movie_df['Movie'] == movie]['Year'].values[0]}")
                            st.write(f"*Rating:* {starred_movie_df[starred_movie_df['Movie'] == movie]['Rating'].values[0]}")
                            
                else:
                    st.write(f"{movies[0]}")
                    st.write(f"*ID:* {starred_movie_df[starred_movie_df['Movie'] == movies[0]]['ID'].values[0]}")
                    st.write(f"*Year:* {starred_movie_df[starred_movie_df['Movie'] == movies[0]]['Year'].values[0]}")
                    st.write(f"*Rating:* {starred_movie_df[starred_movie_df['Movie'] == movies[0]]['Rating'].values[0]}")
                st.write("")

            else:
                st.write("There is no movie where these actors starred together.")
    

# ---------------------------------------------------------------------------------------------

    elif choice == "4":

        genres_choice_query = """
SELECT DISTINCT mi.info AS Genre
FROM movie_info mi
JOIN info_type it ON mi.info_type_id = it.id
WHERE it.info = 'genres';
"""
        genres_choice = query_db(conn, genres_choice_query, None)
        genres = [genre[0] for genre in genres_choice]
        genre_input = st.selectbox("Select a genre from the dropdown menu below:", genres)
        
        if genre_input:
            
            with open('./queries/genre_query.sql', 'r') as file:
                movies_of_genre = file.read()
            movies_of_genre = query_db(conn, movies_of_genre, ('%'+ genre_input +'%',))

            if movies_of_genre:
                movies_of_genre_df = pd.DataFrame(movies_of_genre, columns=['ID', 'Title', 'Kind', 'Year', 'Rating'])
                unique_movies = sorted(movies_of_genre_df['Title'].unique(), key=lambda x: movies_of_genre_df[movies_of_genre_df['Title'] == x]['Rating'].max(), reverse=True)

                st.write(f"### Top-10 movies of the genre **{genre_input}**:")
                for i, movie in enumerate(unique_movies):
                    st.write(f"### **{i+1}. {movie}**")
                    movie_details = movies_of_genre_df[movies_of_genre_df['Title'] == movie]
                    st.write(f"*ID:* {movie_details['ID'].values[0]}")
                    st.write(f"*Year:* {movie_details['Year'].values[0]}")
                    st.write(f"*Kind:* {movie_details['Kind'].values[0]}")

                    ratings = movie_details['Rating'].unique()
                    if len(ratings) > 1:
                        st.write(f"*Ratings:*")
                        with st.expander("Click to expand"):
                            for rating in ratings:
                                st.write(f"* {rating}")
                    else:
                        st.write(f"*Rating:* {ratings[0]}")
                    st.write("")

            else:
                st.write("No movie found with the given genre.")

# ---------------------------------------------------------------------------------------------

    elif choice == "5":
        company_input = st.text_input("Enter a production company")

        if company_input:
            with open('./queries/company_query.sql', 'r') as file:
                company_query = file.read()
            company_movies = query_db(conn, company_query, ('%'+company_input+'%',)) 

            if company_movies:
                company_movies_df = pd.DataFrame(company_movies, columns=['ID', 'Title','Company', 'Year', 'Kind'])
                unique_company = sorted(company_movies_df['Company'].unique())

                if len(unique_company) > 1:
                    selected_company_name = st.selectbox("There are different companies. Select one", unique_company)
                    company_movies_df = company_movies_df[company_movies_df['Company'] == selected_company_name]

                movies = company_movies_df['Title'].unique()

                st.write("### **Movies:**")
                if len(movies) > 1:
                    with st.expander("Click to expand"):
                        for movie in movies:
                            st.write(f"* **{movie}**")
                            st.write(f"*ID:* {company_movies_df[company_movies_df['Title'] == movie]['ID'].values[0]}")

                            companies = "; ".join(company_movies_df[company_movies_df['Title'] == movie]['Company'].unique())
                            st.write(f"*Company:* {companies}")

                            st.write(f"*Year:* {company_movies_df[company_movies_df['Title'] == movie]['Year'].values[0]}")
                            st.write(f"*Kind:* {company_movies_df[company_movies_df['Title'] == movie]['Kind'].values[0]}")
                            
                            
                else:
                    st.write(f"{movies[0]}")
                    st.write(f"*ID:* {company_movies_df[company_movies_df['Title'] == movies[0]]['ID'].values[0]}")
                    companies = "; ".join(company_movies_df[company_movies_df['Title'] == movies[0]]['Company'].unique())
                    st.write(f"*Company:* {companies}")
                    st.write(f"*Year:* {company_movies_df[company_movies_df['Title'] == movies[0]]['Year'].values[0]}")
                    st.write(f"*Kind:* {company_movies_df[company_movies_df['Title'] == movies[0]]['Kind'].values[0]}") 
                st.write("")

            else:
                st.write("No movie found with the given company.")



    # When done with the connection, release it
    release_db_connection(st.session_state.connection_pool, conn)

# Database connection details
if __name__ == "__main__":

    # Define the connection pool outside of main
    if 'connection_pool' not in st.session_state:
        st.sidebar.title("Database Credentials")
        db_user = st.sidebar.text_input("Enter your DB user")
        db_password = st.sidebar.text_input("Enter your DB password", type="password")
        if st.sidebar.button('Connect'):
            st.session_state.connection_pool = create_connection_pool(
                host="localhost", 
                dbname="imdb", 
                user=db_user, 
                password=db_password
            )
            st.sidebar.success('Connected to the database')

    if 'connection_pool' in st.session_state:
        try:
            main()
        except Exception as e:
            st.error(f"An error occurred: {e}")
