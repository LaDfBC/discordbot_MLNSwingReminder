from scouting.pitch_fetcher import run_report_on


def handle_scouting_request(message):
    flags = message.split(",")

    deltas = False
    pitcher = None
    ranges = 100
    for flag in flags:
        if flag.find('pitcher') != -1:
            pitcher = flag[flag.find('pitcher=') + 8:]

        if flag.find('deltas') != -1:
            deltas = True

        if flag.find('ranges') != -1:
            ranges = int(flag[flag.find('ranges') + 7:])

    scouting_info = run_report_on(pitcher, deltas, ranges).to_dict(orient='index')

    response = ''
    for row in scouting_info:
        response += str(row) + " : " + str(scouting_info[row]['count']) + '\n'

    return response

if __name__ == '__main__':
    handle_scouting_request("!scouting pitcher=Syd Kidd,deltas,ranges=50")