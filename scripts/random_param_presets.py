# -*- coding: utf-8 -*-

import json
import os
import random
from decimal import Decimal, ROUND_FLOOR

import gradio as gr
import modules.scripts as scripts


EXT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESET_FILE = os.path.join(EXT_ROOT, "random_param_presets.json")


def decimal_to_clean_string(value):
    if isinstance(value, Decimal):
        s = format(value, "f")
    else:
        s = str(value)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def pick_random_decimal(a, b, step):
    a = Decimal(str(a))
    b = Decimal(str(b))
    step = Decimal(str(step))

    if step <= 0:
        raise ValueError("Step must be greater than 0.")

    low = min(a, b)
    high = max(a, b)

    count = int(((high - low) / step).to_integral_value(rounding=ROUND_FLOOR))
    values = [low + step * i for i in range(count + 1)]
    values = [v for v in values if v <= high]

    if not values:
        raise ValueError("No valid values generated. Check min/max/step.")

    return random.choice(values)


def pick_random_int(a, b, step):
    a = int(a)
    b = int(b)
    step = int(step)

    if step <= 0:
        raise ValueError("Step must be greater than 0.")

    low = min(a, b)
    high = max(a, b)
    values = list(range(low, high + 1, step))

    if not values:
        raise ValueError("No valid integer values generated. Check min/max/step.")

    return random.choice(values)


def load_presets():
    if not os.path.exists(PRESET_FILE):
        return {}

    try:
        with open(PRESET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {}
    except Exception as e:
        print(f"[Random Param Presets] Failed to load presets: {e}")
        return {}


def save_presets(data):
    try:
        with open(PRESET_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Random Param Presets] Failed to save presets: {e}")


def get_preset_names():
    return sorted(load_presets().keys())


class Script(scripts.Script):
    def title(self):
        return "Random CFG / Hires Params + Presets"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        preset_names = get_preset_names()

        with gr.Accordion("Random CFG / Hires Params + Presets", open=False):
            gr.Markdown(
                "Randomize CFG / Hires steps / Hires denoise and save/apply these settings as presets."
            )

            with gr.Group():
                gr.Markdown("### CFG")
                cfg_enabled = gr.Checkbox(label="Enable random CFG", value=False)
                with gr.Row():
                    cfg_min = gr.Number(label="CFG Min / A", value=4.0)
                    cfg_max = gr.Number(label="CFG Max / B", value=5.0)
                    cfg_step = gr.Number(label="CFG Step / C", value=0.1)

            with gr.Group():
                gr.Markdown("### Hires steps")
                hires_steps_enabled = gr.Checkbox(label="Enable random Hires steps", value=False)
                with gr.Row():
                    hires_steps_min = gr.Number(label="Hires steps Min / A", value=5, precision=0)
                    hires_steps_max = gr.Number(label="Hires steps Max / B", value=10, precision=0)
                    hires_steps_step = gr.Number(label="Hires steps Step / C", value=1, precision=0)

            with gr.Group():
                gr.Markdown("### Hires denoise")
                hires_denoise_enabled = gr.Checkbox(label="Enable random Hires denoise", value=False)
                with gr.Row():
                    hires_denoise_min = gr.Number(label="Hires denoise Min / A", value=0.30)
                    hires_denoise_max = gr.Number(label="Hires denoise Max / B", value=0.40)
                    hires_denoise_step = gr.Number(label="Hires denoise Step / C", value=0.01)

            with gr.Group():
                gr.Markdown("### Presets")
                preset_name = gr.Textbox(label="Preset name to save", placeholder="Example: Preset1")
                with gr.Row():
                    preset_dropdown = gr.Dropdown(
                        label="Saved presets",
                        choices=preset_names,
                        value=preset_names[0] if preset_names else None,
                        allow_custom_value=False,
                    )
                with gr.Row():
                    save_btn = gr.Button("Save", variant="primary")
                    apply_btn = gr.Button("Apply")
                    refresh_btn = gr.Button("Refresh List")
                    delete_btn = gr.Button("Delete")
                status = gr.Markdown("")

            def on_save_preset(
                name,
                cfg_enabled_v,
                cfg_min_v,
                cfg_max_v,
                cfg_step_v,
                hs_enabled_v,
                hs_min_v,
                hs_max_v,
                hs_step_v,
                hd_enabled_v,
                hd_min_v,
                hd_max_v,
                hd_step_v,
            ):
                name = (name or "").strip()
                if not name:
                    return gr.update(), "Please enter a preset name."

                data = load_presets()
                data[name] = {
                    "cfg_enabled": bool(cfg_enabled_v),
                    "cfg_min": cfg_min_v,
                    "cfg_max": cfg_max_v,
                    "cfg_step": cfg_step_v,
                    "hires_steps_enabled": bool(hs_enabled_v),
                    "hires_steps_min": hs_min_v,
                    "hires_steps_max": hs_max_v,
                    "hires_steps_step": hs_step_v,
                    "hires_denoise_enabled": bool(hd_enabled_v),
                    "hires_denoise_min": hd_min_v,
                    "hires_denoise_max": hd_max_v,
                    "hires_denoise_step": hd_step_v,
                }
                save_presets(data)
                names = sorted(data.keys())
                return gr.update(choices=names, value=name), f"Preset saved: **{name}**"

            def on_apply_preset(name):
                data = load_presets()
                if not name or name not in data:
                    return (
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        "Preset not found.",
                    )

                preset = data[name]
                return (
                    preset.get("cfg_enabled", False),
                    preset.get("cfg_min", 4.0),
                    preset.get("cfg_max", 5.0),
                    preset.get("cfg_step", 0.1),
                    preset.get("hires_steps_enabled", False),
                    preset.get("hires_steps_min", 5),
                    preset.get("hires_steps_max", 10),
                    preset.get("hires_steps_step", 1),
                    preset.get("hires_denoise_enabled", False),
                    preset.get("hires_denoise_min", 0.30),
                    preset.get("hires_denoise_max", 0.40),
                    preset.get("hires_denoise_step", 0.01),
                    name,
                    f"Preset applied: **{name}**",
                )

            def on_refresh_list():
                names = get_preset_names()
                return gr.update(choices=names, value=names[0] if names else None), "Preset list refreshed."

            def on_delete_preset(name):
                data = load_presets()
                if not name or name not in data:
                    return gr.update(), gr.update(), "Preset not found."

                del data[name]
                save_presets(data)
                names = sorted(data.keys())
                return (
                    gr.update(choices=names, value=names[0] if names else None),
                    "",
                    f"Preset deleted: **{name}**",
                )

            def on_dropdown_change(name):
                return name or ""

            save_btn.click(
                fn=on_save_preset,
                inputs=[
                    preset_name,
                    cfg_enabled,
                    cfg_min,
                    cfg_max,
                    cfg_step,
                    hires_steps_enabled,
                    hires_steps_min,
                    hires_steps_max,
                    hires_steps_step,
                    hires_denoise_enabled,
                    hires_denoise_min,
                    hires_denoise_max,
                    hires_denoise_step,
                ],
                outputs=[preset_dropdown, status],
            )

            apply_btn.click(
                fn=on_apply_preset,
                inputs=[preset_dropdown],
                outputs=[
                    cfg_enabled,
                    cfg_min,
                    cfg_max,
                    cfg_step,
                    hires_steps_enabled,
                    hires_steps_min,
                    hires_steps_max,
                    hires_steps_step,
                    hires_denoise_enabled,
                    hires_denoise_min,
                    hires_denoise_max,
                    hires_denoise_step,
                    preset_name,
                    status,
                ],
            )

            refresh_btn.click(fn=on_refresh_list, inputs=[], outputs=[preset_dropdown, status])
            delete_btn.click(fn=on_delete_preset, inputs=[preset_dropdown], outputs=[preset_dropdown, preset_name, status])
            preset_dropdown.change(fn=on_dropdown_change, inputs=[preset_dropdown], outputs=[preset_name])

        return [
            cfg_enabled,
            cfg_min,
            cfg_max,
            cfg_step,
            hires_steps_enabled,
            hires_steps_min,
            hires_steps_max,
            hires_steps_step,
            hires_denoise_enabled,
            hires_denoise_min,
            hires_denoise_max,
            hires_denoise_step,
        ]

    def process(
        self,
        p,
        cfg_enabled,
        cfg_min,
        cfg_max,
        cfg_step,
        hires_steps_enabled,
        hires_steps_min,
        hires_steps_max,
        hires_steps_step,
        hires_denoise_enabled,
        hires_denoise_min,
        hires_denoise_max,
        hires_denoise_step,
    ):
        if not hasattr(p, "extra_generation_params") or p.extra_generation_params is None:
            p.extra_generation_params = {}

        try:
            if cfg_enabled:
                chosen_cfg = pick_random_decimal(cfg_min, cfg_max, cfg_step)
                p.cfg_scale = float(chosen_cfg)
                p.extra_generation_params["Random CFG"] = decimal_to_clean_string(chosen_cfg)
                print(f"[Random Param Presets] CFG Scale set to: {chosen_cfg}")
        except Exception as e:
            print(f"[Random Param Presets] CFG error: {e}")

        if getattr(p, "enable_hr", False):
            try:
                if hires_steps_enabled:
                    chosen_steps = pick_random_int(hires_steps_min, hires_steps_max, hires_steps_step)
                    p.hr_second_pass_steps = int(chosen_steps)
                    p.extra_generation_params["Random Hires steps"] = str(chosen_steps)
                    print(f"[Random Param Presets] Hires steps set to: {chosen_steps}")
            except Exception as e:
                print(f"[Random Param Presets] Hires steps error: {e}")

            try:
                if hires_denoise_enabled:
                    chosen_denoise = pick_random_decimal(
                        hires_denoise_min,
                        hires_denoise_max,
                        hires_denoise_step,
                    )
                    p.denoising_strength = float(chosen_denoise)
                    p.extra_generation_params["Random Hires denoise"] = decimal_to_clean_string(chosen_denoise)
                    print(f"[Random Param Presets] Hires denoise set to: {chosen_denoise}")
            except Exception as e:
                print(f"[Random Param Presets] Hires denoise error: {e}")
        else:
            if hires_steps_enabled or hires_denoise_enabled:
                print("[Random Param Presets] Hires fix is OFF, so Hires parameters were skipped.")
