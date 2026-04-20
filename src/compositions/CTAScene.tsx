import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { STYLES, type StyleName } from "../lib/styles";

export const CTAScene: React.FC<{
  title: string;
  subtitle: string;
  style?: StyleName;
}> = ({ title, subtitle, style = "viral" }) => {
  const frame = useCurrentFrame();
  const s = STYLES[style];

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleScale = interpolate(frame, [0, 20], [0.8, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  const subOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" });
  const buttonOpacity = interpolate(frame, [30, 50], [0, 1], { extrapolateRight: "clamp" });
  const buttonY = interpolate(frame, [30, 50], [20, 0], { extrapolateRight: "clamp" });
  const pulseScale = 1 + Math.sin(frame * 0.05) * 0.03;

  return (
    <AbsoluteFill style={{ background: s.bg, fontFamily: s.font, color: s.text, overflow: "hidden" }}>
      {/* Radial glow */}
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(ellipse at 50% 50%, ${s.accent}15, transparent 60%)` }} />

      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ opacity: titleOpacity, transform: `scale(${titleScale})`, textAlign: "center" }}>
          <h1 style={{ fontSize: 80, fontWeight: 900, margin: 0, lineHeight: 1.05, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            {title}
          </h1>
        </div>

        <div style={{ opacity: subOpacity, marginTop: 24 }}>
          <p style={{ fontSize: 24, color: s.muted, fontWeight: 500, margin: 0 }}>{subtitle}</p>
        </div>

        <div style={{ opacity: buttonOpacity, transform: `translateY(${buttonY}px) scale(${pulseScale})`, marginTop: 48 }}>
          <div style={{ padding: "18px 48px", borderRadius: 16, background: s.gradient, fontSize: 24, fontWeight: 700, color: "#fff" }}>
            Get Started →
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};