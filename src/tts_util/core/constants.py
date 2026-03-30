from types import MappingProxyType
from typing import Final, Mapping

TEXT_REPLACEMENTS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "\r": "",  # Normalize line endings
        "-\n": "",  # Join continued words
        "\n": " ",  # Join multiline sentences
        "Fig. ": "Figure ",
        "Eq. ": "Equation ",
        "\\displaystyle": "",
        "×": "times",
        "∈": "in",
        "=": "equals",
        "≈": "almost equals",
        "⊂": "subset",
        "⊆": "subset",
        "∩": "intersection",
        "∪": "union",
        "→": "to",
        "δ": "delta",
        "η": "eta",
        "λ": "lambda",
        "µ": "mu",
        "Ω": "omega",
        "τ": "tau",
        "θ": "theta",
        "σ": "sigma",
        "ĥ": "h hat",
        "ŷ": "y hat",
        "−": "minus",
    }
)
