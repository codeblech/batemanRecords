import math
from typing import TypedDict
from app.config import console


class HeatmapPoint(TypedDict):
    start_time: float
    end_time: float
    value: float


class HottestSegment(TypedDict):
    start_time: float
    end_time: float
    average_heat: float
    segment_data: list[HeatmapPoint]


def find_hottest_segment(
    data: list[HeatmapPoint], target_duration: float = 30.0
) -> HottestSegment:
    console.print(
        f"Analyzing [bold]{len(data)}[/bold] heatmap points to find hottest [bold]{target_duration:.0f}s[/bold] segment"
    )
    # 1. Calculate average duration of one data point
    # (Assuming uniform duration, but good to be safe)
    avg_step = (data[-1]["end_time"] - data[0]["start_time"]) / len(data)

    # 2. Calculate how many points we need for the target duration
    # We use ceil (round up) to ensure we cover at least the target time
    points_needed = math.ceil(target_duration / avg_step)

    max_sum = -1
    best_start_index = -1

    # 3. Sliding Window Loop
    # We stop the loop when the window would go past the end of the list
    for i in range(len(data) - points_needed + 1):
        # Extract the window
        current_window = data[i : i + points_needed]

        # Calculate the "heat" (sum of values)
        current_sum = sum(item["value"] for item in current_window)

        # Check if this is the new best
        if current_sum > max_sum:
            max_sum = current_sum
            best_start_index = i

    # 4. Retrieve the result
    best_segment = data[best_start_index : best_start_index + points_needed]
    console.print(
        f"Hottest segment starts at [bold]{best_segment[0]['start_time']:.2f}s[/bold] and ends at [bold]{best_segment[-1]['end_time']:.2f}s[/bold]"
    )

    return {
        "start_time": best_segment[0]["start_time"],
        "end_time": best_segment[-1]["end_time"],
        "average_heat": max_sum / points_needed,
        "segment_data": best_segment,
    }
