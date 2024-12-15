import json

json_fuzzy_temp = """
{
  "температура": [
      {
      "id": "холодно",
      "points": [
          [0,1],
          [18,1],
          [22,0],
          [50,0]
      ]
      },
      {
      "id": "комфортно",
      "points": [
          [18,0],
          [22,1],
          [24,1],
          [26,0]
      ]
      },
      {
      "id": "жарко",
      "points": [
          [0,0],
          [24,0],
          [26,1],
          [50,1]
      ]
      }
  ]
}
"""

json_fuzzy_heat = """
{
  "температура": [
      {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
      },
      {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
      },
      {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
      }
  ]
}
"""

json_fuzzy_rules = """
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
] 
"""


def build_fuzzy_functions(json_data):
    data = json.loads(json_data)
    fuzzy_functions = {}

    for item in data["температура"]:
        term = item["id"]
        points = item["points"]

        def membership_function(x, points=points):
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                if x1 <= x <= x2:
                    if x2 - x1 == 0:
                        return y1
                    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
            return 0.0

        fuzzy_functions[term] = membership_function

    return fuzzy_functions


def defuzzify(output_memberships, membership_functions):
    numerator = 0.0
    denominator = 0.0

    for term, degree in output_memberships.items():
        mf = membership_functions[term]
        for point in range(0, 51): 
            numerator += mf(point) * point * degree
            denominator += mf(point) * degree

    if denominator == 0.0:
        return 0.0
    return numerator / denominator


def main(json_fuzzy_temp, json_fuzzy_heat, json_fuzzy_rules, value):
    temp_memberships = build_fuzzy_functions(json_fuzzy_temp)
    heat_memberships = build_fuzzy_functions(json_fuzzy_heat)

    fuzzy_rules = json.loads(json_fuzzy_rules)

    input_memberships = {}
    for temp_term, mf in temp_memberships.items():
        input_memberships[temp_term] = mf(value)

    output_memberships = {}
    for rule in fuzzy_rules:
        temp_term, heat_term = rule
        degree = input_memberships.get(temp_term, 0.0)
        if heat_term not in output_memberships:
            output_memberships[heat_term] = 0.0
        output_memberships[heat_term] = max(output_memberships[heat_term], degree)

    result = defuzzify(output_memberships, heat_memberships)

    return result


if __name__ == "__main__":
    res = main(json_fuzzy_temp, json_fuzzy_heat, json_fuzzy_rules, 20)
    print(round(res, 3))