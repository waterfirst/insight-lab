"""Reproduce the data figures used in sp12_ai_literacy.qmd.

Sources
-------
1. Dell'Acqua et al., HBS Working Paper 24-013.
2. World Economic Forum, Future of Jobs Report 2025, Figure 3.3.

The HBS outcomes use different dependent variables and units.  The chart keeps
the reported values together only to show the direction of the jagged frontier;
they must not be summed or treated as a common effect size.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


HERE = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "Noto Sans CJK KR"
plt.rcParams["axes.unicode_minus"] = False


def save_jagged_frontier() -> None:
    frontier = pd.DataFrame(
        {
            "결과": ["완료 과제 수", "작업 속도", "평가 품질", "경계 밖 정확성"],
            "변화": [12.2, 25.1, 40.0, -19.0],
            "단위": ["%", "%", "% 이상", "%p"],
        }
    )

    fig, ax = plt.subplots(figsize=(10, 5.6))
    colors = ["#6d42a6" if value > 0 else "#dc4b43" for value in frontier["변화"]]
    bars = ax.barh(frontier["결과"], frontier["변화"], color=colors, height=0.62)
    ax.axvline(0, color="#334155", linewidth=1)
    ax.set_xlim(-25, 48)
    ax.set_xlabel("대조군 대비 보고된 변화")
    ax.set_title(
        "생산성 향상과 정확성 하락이 같은 실험에 공존한다",
        loc="left",
        weight="bold",
        fontsize=16,
    )
    ax.text(
        -25,
        4.0,
        "758명 컨설턴트 무작위 배정 · HBS/BCG",
        color="#64748b",
        fontsize=10,
    )
    for bar, value, unit in zip(bars, frontier["변화"], frontier["단위"]):
        x = value + (1.2 if value >= 0 else -1.2)
        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            f"{value:+.1f}{unit}",
            va="center",
            ha="left" if value >= 0 else "right",
            weight="bold",
            color="#172033",
        )
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.18)
    fig.tight_layout()
    fig.savefig(HERE / "sp12_jagged_frontier.svg", bbox_inches="tight")
    plt.close(fig)


def save_wef_skills() -> None:
    skills = pd.DataFrame(
        {
            "역량": ["분석적 사고", "기술 문해력", "AI·빅데이터", "다언어 능력", "프로그래밍"],
            "응답률": [69, 51, 45, 23, 17],
        }
    ).sort_values("응답률")

    fig, ax = plt.subplots(figsize=(10, 5.4))
    colors = ["#b69ad8", "#a889ce", "#8a67be", "#7650a8", "#62418f"]
    bars = ax.barh(skills["역량"], skills["응답률"], color=colors)
    ax.set_xlim(0, 76)
    ax.set_xlabel("해당 역량을 핵심으로 본 고용주 비율 (%)")
    ax.set_title(
        "AI 시대의 핵심은 단일 기술이 아니라 판단–기술의 조합",
        loc="left",
        weight="bold",
        fontsize=16,
    )
    ax.text(
        0,
        5.0,
        "World Economic Forum · Future of Jobs Report 2025",
        color="#64748b",
        fontsize=10,
    )
    for bar, value in zip(bars, skills["응답률"]):
        ax.text(
            value + 1.2,
            bar.get_y() + bar.get_height() / 2,
            f"{value}%",
            va="center",
            weight="bold",
        )
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.18)
    fig.tight_layout()
    fig.savefig(HERE / "sp12_wef_skills.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    save_jagged_frontier()
    save_wef_skills()
