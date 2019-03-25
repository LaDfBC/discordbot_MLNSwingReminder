class Post:
    def __init__(self, post):
        self.post = post
        self.is_game_day_thread = True
        try:
            self.__assign_teams__()  # Assigns variables self.team_name_one and self.team_name_two
            self.users_to_position_players = self.__fetch_position_players__()
        except ValueError:
            self.is_game_day_thread = False

    def is_game_thread(self):
        return self.is_game_day_thread

    def get_last_comment_time(self):
        if self.__is_game_day_thread__():
            # We're returning this sucker.  It has every pitch in the game (hopefully!)

            # Start pulling pitches and adding them to the list
            for comment in self.post.comments:
                # Figure out which player is batting
                return comment.created

    def get_users(self):
        return self.users_to_position_players.keys()

    def __assign_teams__(self):
        text = self.post.selftext
        teams = {}

        smallest_index = 100000
        all_indexes = []
        for abbreviation in get_team_abbreviation_list():
            index = text.find(abbreviation)
            if index != -1:
                teams[abbreviation] = index
                all_indexes.append(index)
                if index < smallest_index:
                    smallest_index = index

        # This is bad - I originally threw an error, but realized I could just knock it down
        if len(teams) > 2:
            teams_to_pop = []
            all_indexes = sorted(all_indexes)
            for team in teams:
                if not teams[team] == all_indexes[0] and not teams[team] == all_indexes[1]:
                    teams_to_pop.append(team)

            for team_to_pop in teams_to_pop:
                teams.pop(team_to_pop)
        elif len(teams) < 2:
            raise ValueError("Couldn't find enough teams!")

        for team in teams:
            if teams[team] == smallest_index:
                self.team_name_one = team
            else:
                self.team_name_two = team

    # Hoo boy, this is the nasty function
    def get_current_player(self):
        if self.__is_game_day_thread__():
            # We're returning this sucker.  It has every pitch in the game (hopefully!)
            comment = self.post.comments[-1] # Very last one
            # Figure out which player is batting
            return self.__get_player_from_comment__(comment)

    def get_current_pitcher(self):
        return pitchers

    def has_current_player_swung(self):
        # No comments here - move along...
        if len(self.post.comments) == 0:
            return False

        first_comment = self.post.comments[-1]
        # Toplevel comment is not a player, so we assume it's a pitcher or some random idiot
        if first_comment is None:
            return False
        if self.__get_player_from_comment__(first_comment) is None:
            return False
        # True if there's at least one comment, false otherwise
        return len(first_comment.replies) > 0

    '''
    True if this thread is a GDT, false otherwise.
    '''
    def __is_game_day_thread__(self):
        return self.post.link_flair_text == 'Exhibition Game' or \
            self.post.link_flair_text[-8:] == 'Game Day' or \
            self.post.link_flair_text == 'Winter Training' or \
            'GotS' in self.post.link_flair_text

    @staticmethod
    def __get_player_from_comment__(comment):
        comment_text = comment.body.replace(" ", "")
        player_open_index = comment_text.find("[")
        player_close_index = comment_text.find("]", player_open_index)

        if player_open_index == -1:
            return None

        username_open_index = comment_text.find("(/u", player_close_index)
        username_close_index = comment_text.find(")", username_open_index)
        return comment_text[username_open_index + 1: username_close_index].lower()

    def __fetch_position_players__(self):
        text = self.post.selftext

        players = {self.team_name_one: {}, self.team_name_two: {}}

        box_index = text.find("BOX")
        if box_index == -1:
            box_index = text.find("Box")
        batters_index = box_index + 8

        first_team = True
        # Scrapes the table of players to get each of them and assign them to a team
        while text.find("[", batters_index) != -1:
            # This is watching for replaced team members. Otherwise, we have issues with parsing
            triple_pipe_check = text.find("|||", batters_index)
            batter_open_index = text.find("[", batters_index)
            batter_close_index = text.find("]", batter_open_index)
            batter_name = text[batter_open_index + 1: batter_close_index]

            if triple_pipe_check != -1 and triple_pipe_check < batter_open_index:
                first_team = not first_team

            username_open_index = text.find("(", batter_close_index)
            username_close_index = text.find(")", username_open_index)
            username = text[username_open_index + 1: username_close_index].lower().replace(" ", "")

            if first_team:
                players[self.team_name_one][username] = batter_name
            else:
                players[self.team_name_two][username] = batter_name
            first_team = not first_team

            batters_index = batter_close_index

        return players

    #TODO - broke as hell
    def __fetch_pitchers__(self):
        pitchers_index = 0
        text = self.post.selftext

        text.find("Pitchers")

        # This is watching for replaced team members. Otherwise, we have issues with parsing
        triple_pipe_check = text.find("|||", pitchers_index)
        batter_open_index = text.find("[", pitchers_index)
        batter_close_index = text.find("]", batter_open_index)
        batter_name = text[batter_open_index + 1: batter_close_index]

        if triple_pipe_check != -1 and triple_pipe_check < batter_open_index:
            first_team = not first_team

        username_open_index = text.find("(", batter_close_index)
        username_close_index = text.find(")", username_open_index)
        username = text[username_open_index + 1: username_close_index].lower().replace(" ", "")

        if first_team:
            players[self.team_name_one][username] = batter_name
        else:
            players[self.team_name_two][username] = batter_name
        first_team = not first_team

        batters_index = batter_close_index


def get_team_abbreviation_list():
    return [
        'ACP', 'ANA', 'BFB', 'CIN',
        'MAL', 'SUN', 'GHG', 'EXP',
        'SMD', 'VAN', 'KYM', 'POP',
        'SHH', 'POR', 'HMH', 'LPJ'
    ]