"""
pccx — Deterministic Architecture Diagram Generator.

Provides directives to generate bit-accurate architectural SVG diagrams
(PE arrays, memory layouts) directly from configuration.
"""

from __future__ import annotations

import textwrap
from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx

__version__ = "0.1.0"

# Canonical pccx diagram palette.
PALETTE = {
    "panel-host": "#dae7f4",
    "panel-dram": "#f5edd5",
    "panel-pl":   "#fafafa",
    "block-ctrl": "#fce5c6",
    "block-comp": "#ffffff",
    "block-mem":  "#e2efd8",
    "block-bus":  "#ebebeb",
}

class PEArrayDirective(Directive):
    """
    Directive to generate a PE array SVG.
    Usage:
    .. pccx-pe-array::
       :rows: 4
       :cols: 4
       :mode: weight-stationary
    """
    has_content = False
    option_spec = {
        'rows': directives.positive_int,
        'cols': directives.positive_int,
        'mode': lambda x: directives.choice(x, ('weight-stationary', 'weight-streaming')),
        'show-arrows': directives.flag,
    }

    def run(self) -> List[nodes.Node]:
        rows = self.options.get('rows', 4)
        cols = self.options.get('cols', 4)
        mode = self.options.get('mode', 'weight-stationary')
        show_arrows = 'show-arrows' in self.options

        # Adjust dimensions to accommodate arrows
        box_w, box_h = 70, 48
        gap_x, gap_y = 30, 25
        width = cols * (box_w + gap_x) + 50
        height = rows * (box_h + gap_y) + 50
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" class="pccx-diagram">',
            f'  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
            '  <defs>',
            '    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">',
            '      <path d="M0,0 L10,5 L0,10 z" fill="#000000"/>',
            '    </marker>',
            '  </defs>',
            '  <style>',
            '    .block-comp { fill: #ffffff; stroke: #000000; stroke-width: 0.8; }',
            '    .text-pe { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 11px; text-anchor: middle; font-weight: 600; }',
            '    .line-flow { stroke: #000000; stroke-width: 0.8; fill: none; marker-end: url(#arr); }',
            '  </style>'
        ]

        for r in range(rows):
            for c in range(cols):
                x = 40 + c * (box_w + gap_x)
                y = 40 + r * (box_h + gap_y)
                svg_parts.append(f'  <rect class="block-comp" x="{x}" y="{y}" width="{box_w}" height="{box_h}"/>')
                svg_parts.append(f'  <text class="text-pe" x="{x+box_w/2}" y="{y+box_h/2+4}">PE[{r},{c}]</text>')

                if show_arrows:
                    # Right arrow (Activation)
                    if c < cols - 1:
                        svg_parts.append(f'  <line class="line-flow" x1="{x+box_w}" y1="{y+box_h/2}" x2="{x+box_w+gap_x-2}" y2="{y+box_h/2}"/>')
                    # Down arrow (Partial Sum)
                    if r < rows - 1:
                        svg_parts.append(f'  <line class="line-flow" x1="{x+box_w/2}" y1="{y+box_h}" x2="{x+box_w/2}" y2="{y+box_h+gap_y-2}"/>')

        svg_parts.append('</svg>')
        
        raw_node = nodes.raw('', '\n'.join(svg_parts), format='html')
        return [raw_node]

class MemoryLayoutDirective(Directive):
    """
    Directive to generate a memory layout/bank diagram.
    Usage:
    .. pccx-memory-layout::
       :banks: 8
       :depth: 4
       :title: L2 Shared Buffer (URAM)
    """
    has_content = True
    option_spec = {
        'banks': directives.positive_int,
        'depth': directives.positive_int,
        'title': directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        banks = self.options.get('banks', 8)
        depth = self.options.get('depth', 4)
        title = self.options.get('title', 'Memory Layout')
        
        box_w = 60
        box_h = 30
        width = banks * (box_w + 5) + 100
        height = depth * (box_h + 5) + 80

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" class="pccx-diagram">',
            f'  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
            '  <style>',
            '    .block-mem { fill: #e2efd8; stroke: #000000; stroke-width: 0.8; }',
            '    .text-main { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 12px; }',
            '    .text-label { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 10px; text-anchor: middle; }',
            '    .text-title { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 13px; font-weight: bold; text-anchor: middle; }',
            '  </style>',
            f'  <text class="text-title" x="{width/2}" y="25">{title}</text>'
        ]

        # Draw banks
        for b in range(banks):
            svg_parts.append(f'  <text class="text-label" x="{50 + b*(box_w+5) + box_w/2}" y="45">Bank {b}</text>')
            for d in range(depth):
                x = 50 + b * (box_w + 5)
                y = 55 + d * (box_h + 5)
                svg_parts.append(f'  <rect class="block-mem" x="{x}" y="{y}" width="{box_w}" height="{box_h}"/>')
                if b == 0:
                    svg_parts.append(f'  <text class="text-label" x="25" y="{y + box_h/2 + 4}" text-anchor="middle">Row {d}</text>')

        svg_parts.append('</svg>')
        raw_node = nodes.raw('', '\n'.join(svg_parts), format='html')
        return [raw_node]

class BitPackingDirective(Directive):
    """
    Directive to visualize bit-level packing.
    Usage:
    .. pccx-bit-packing::
       :title: DSP48E2 Port A (27-bit) Packing
    """
    has_content = False
    option_spec = {
        'title': directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        title = self.options.get('title', 'Bit Packing Layout')
        
        bits = 27
        box_w = 20
        box_h = 30
        width = bits * box_w + 100
        height = 120

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" class="pccx-diagram">',
            f'  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
            '  <style>',
            '    .bit-box { fill: #ffffff; stroke: #000000; stroke-width: 0.8; }',
            '    .bit-w1  { fill: #dae7f4; stroke: #000000; stroke-width: 0.8; }',
            '    .bit-w2  { fill: #e2efd8; stroke: #000000; stroke-width: 0.8; }',
            '    .bit-g   { fill: #ebebeb; stroke: #000000; stroke-width: 0.8; }',
            '    .text-idx { fill: #666666; font-family: ui-sans-serif, system-ui; font-size: 9px; text-anchor: middle; }',
            '    .text-label { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 11px; text-anchor: middle; }',
            '    .text-title { fill: #000000; font-family: ui-sans-serif, system-ui; font-size: 13px; font-weight: bold; text-anchor: middle; }',
            '  </style>',
            f'  <text class="text-title" x="{width/2}" y="25">{title}</text>'
        ]

        # Draw bit boxes (0 to 26)
        for i in range(bits):
            idx = bits - 1 - i # MSB to LSB
            x = 50 + i * box_w
            y = 45
            
            # Color logic
            cls = "bit-box"
            lbl = ""
            if 22 <= idx <= 26: cls, lbl = "bit-w1", f"W1[{idx-22}]"
            elif 4 <= idx <= 21: cls, lbl = "bit-g", "G"
            elif 0 <= idx <= 3:  cls, lbl = "bit-w2", f"W2[{idx}]"
            
            svg_parts.append(f'  <rect class="{cls}" x="{x}" y="{y}" width="{box_w}" height="{box_h}"/>')
            svg_parts.append(f'  <text class="text-idx" x="{x+box_w/2}" y="{y-5}">{idx}</text>')
            if lbl:
                svg_parts.append(f'  <text class="text-label" x="{x+box_w/2}" y="{y+box_h+15}" transform="rotate(45 {x+box_w/2} {y+box_h+15})">{lbl}</text>')

        svg_parts.append('</svg>')
        raw_node = nodes.raw('', '\n'.join(svg_parts), format='html')
        return [raw_node]

def setup(app: Sphinx) -> dict:
    app.add_directive("pccx-pe-array", PEArrayDirective)
    app.add_directive("pccx-memory-layout", MemoryLayoutDirective)
    app.add_directive("pccx-bit-packing", BitPackingDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
