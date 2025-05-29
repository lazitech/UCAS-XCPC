import sys
from datetime import datetime


def ghost_to_xml(ghost_file, start_time, output_file):
    # 解析ghost文件
    contest_name = ""
    contlen_min = 0
    problems = []
    teams = []
    regions = {}  # {region_id: school_name}
    submissions = []

    with open(ghost_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ', 1)
            if parts[0] == '@contest':
                contest_name = parts[1].strip('"')
            elif parts[0] == '@contlen':
                contlen_min = int(parts[1])
            elif parts[0] == '@p':
                p_parts = parts[1].split(',')
                letter = p_parts[0]
                name = p_parts[1]
                problems.append({'letter': letter, 'name': name})
            elif parts[0] == '@t':
                t_parts = parts[1].split(',')
                team_id = t_parts[0]
                region_id = t_parts[2]
                team_name = ','.join(t_parts[3:])  # 处理可能包含逗号的情况
                # 分割学校和姓名
                if '-' in team_name:
                    school, name = team_name.rsplit('-', 1)
                else:
                    school = "Unknown School"
                    name = team_name
                regions[region_id] = school.strip()
                teams.append({
                    'id': team_id,
                    'external_id': team_id,
                    'region_id': region_id,
                    'name': name.strip(),
                    'school': school.strip()
                })
            elif parts[0] == '@s':
                s_parts = parts[1].split(',')
                team_id = s_parts[0]
                problem_letter = s_parts[1]
                time_sec = s_parts[3]
                result = s_parts[4]
                submissions.append({
                    'team_id': team_id,
                    'problem': problem_letter,
                    'time': float(time_sec),
                    'result': result
                })

    # 处理start_time
    try:
        start_time = float(start_time)
    except:
        # 尝试解析时间字符串
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp()

    # 生成XML各部分
    xml = ['<contest>']

    # Info
    xml.append('<info>')
    xml.append(f'  <length>{contlen_min // 60}:{contlen_min % 60:02}:00</length>')
    xml.append('  <penalty>20</penalty>')
    xml.append('  <started>False</started>')
    xml.append(f'  <starttime>{start_time}</starttime>')
    xml.append(f'  <title>{contest_name}</title>')
    xml.append(f'  <short-title>{contest_name}</short-title>')
    xml.append('  <scoreboard-freeze-length>0:30:00</scoreboard-freeze-length>')
    xml.append('  <contest-id>default--3</contest-id>')
    xml.append('</info>')

    # Regions
    for rid, rname in regions.items():
        xml.append('<region>')
        xml.append(f'  <external-id>{rid}</external-id>')
        xml.append(f'  <name>{rname}</name>')
        xml.append('</region>')

    # Judgements
    xml.append("""
<judgement>
    <id>1</id>
    <acronym>AC</acronym>
    <name>Yes</name>
    <solved>true</solved>
    <penalty>false</penalty>
</judgement>
<judgement>
    <id>2</id>
    <acronym>WA</acronym>
    <name>No - Wrong Answer</name>
    <solved>false</solved>
    <penalty>true</penalty>
</judgement>
<judgement>
    <id>3</id>
    <acronym>CE</acronym>
    <name>No - Compile Error</name>
    <solved>false</solved>
    <penalty>false</penalty>
</judgement>""")

    # Languages
    xml.append("""
<language>
    <id>1</id>
    <name>C</name>
</language>
<language>
    <id>2</id>
    <name>C++</name>
</language>
<language>
    <id>3</id>
    <name>Java</name>
</language>""")

    # Problems
    for idx, p in enumerate(problems, 1):
        xml.append(f"""
<problem>
    <id>{idx}</id>
    <letter>{p['letter']}</letter>
    <name>{p['name']}</name>
</problem>""")

    # Teams
    for t in teams:
        xml.append(f"""
<team>
    <id>{t['id']}</id>
    <external-id>{t['external_id']}</external-id>
    <region>{regions[t['region_id']]}</region>
    <name>{t['name']}</name>
    <university>{t['school']}</university>
</team>""")

    # Runs
    run_id = 1
    for sub in submissions:
        # Find problem id
        problem_id = None
        for idx, p in enumerate(problems, 1):
            if p['letter'] == sub['problem']:
                problem_id = idx
                break

        # Determine judgement
        if sub['result'] == 'AC':
            result = 'AC'
            solved = 'true'
            penalty = 'false'
        else:
            result = 'WA'
            solved = 'false'
            penalty = 'true'

        timestamp = start_time + sub['time']

        xml.append(f"""
<run>
    <id>{run_id}</id>
    <judged>True</judged>
    <language>C++</language>
    <problem>{problem_id}</problem>
    <status>done</status>
    <team>{sub['team_id']}</team>
    <time>{sub['time']:.6f}</time>
    <timestamp>{timestamp:.6f}</timestamp>
    <solved>{solved}</solved>
    <penalty>{penalty}</penalty>
    <result>{result}</result>
</run>""")
        run_id += 1

    # Finalized
    end_time = start_time + contlen_min * 60
    xml.append(f"""
<finalized>
    <last_gold>1</last_gold>
    <last_silver>4</last_silver>
    <last_bronze>9</last_bronze>
    <time>0</time>
    <timestamp>{end_time:.1f}</timestamp>
</finalized>""")

    xml.append('</contest>')

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ghost2xml.py <ghost_file> <start_time> <output_file>")
        print("Example: python ghost2xml.py contest.ghost '2023-12-01 09:00:00' output.xml")
        sys.exit(1)

    ghost_file = sys.argv[1]
    start_time = sys.argv[2]
    output_file = sys.argv[3]

    ghost_to_xml(ghost_file, start_time, output_file)
