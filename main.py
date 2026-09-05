import pygame
import asyncio
import random
import math

# ==========================================
# SETTINGS
# ==========================================

WIDTH = 510
HEIGHT = 830
FPS = 60

# ==========================================
# MAIN
# ==========================================

async def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DPK Particle Animation")

    clock = pygame.time.Clock()

    # ======================================
    # LOAD IMAGE
    # ======================================

    try:
        image = pygame.image.load(
            "assets/DPK.png"
        ).convert_alpha()

        print("DPK image loaded successfully!")

    except Exception as e:

        print("IMAGE ERROR:")
        print(e)

        # Temporary image if loading fails
        image = pygame.Surface(
            (400, 600),
            pygame.SRCALPHA
        )

        image.fill((30, 30, 30, 255))

    # ======================================
    # RESIZE IMAGE
    # ======================================

    max_width = 400
    max_height = 650

    iw, ih = image.get_size()

    scale = min(
        max_width / iw,
        max_height / ih
    )

    new_width = int(iw * scale)
    new_height = int(ih * scale)

    image = pygame.transform.smoothscale(
        image,
        (new_width, new_height)
    )

    image_x = (WIDTH - new_width) // 2
    image_y = (HEIGHT - new_height) // 2

    # ======================================
    # CREATE PARTICLES
    # ======================================

    particles = []

    gap = 7

    for y in range(0, new_height, gap):

        for x in range(0, new_width, gap):

            color = image.get_at((x, y))

            if color.a < 80:
                continue

            if color.r + color.g + color.b < 30:
                continue

            particles.append({
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(0, HEIGHT),

                "tx": image_x + x,
                "ty": image_y + y,

                "color": (
                    color.r,
                    color.g,
                    color.b
                ),

                "size": random.randint(1, 3),

                "speed": random.uniform(
                    0.002,
                    0.006
                ),

                "delay": random.uniform(
                    0,
                    5
                ),

                "phase": random.uniform(
                    0,
                    math.pi * 2
                )
            })

    print("Particles:", len(particles))

    # ======================================
    # SPARKLES
    # ======================================

    sparkles = []

    for i in range(80):

        sparkles.append({
            "x": random.randint(
                0,
                WIDTH
            ),

            "y": random.randint(
                0,
                HEIGHT
            ),

            "size": random.randint(
                1,
                2
            ),

            "phase": random.uniform(
                0,
                math.pi * 2
            )
        })

    # ======================================
    # GAME VARIABLES
    # ======================================

    running = True
    time_passed = 0

    # ======================================
    # GAME LOOP
    # ======================================

    while running:

        dt = clock.tick(FPS) / 1000

        time_passed += dt

        # ----------------------------------
        # EVENTS
        # ----------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # ----------------------------------
        # BACKGROUND
        # ----------------------------------

        screen.fill(
            (5, 5, 12)
        )

        # ----------------------------------
        # PARTICLES
        # ----------------------------------

        for p in particles:

            if time_passed < p["delay"]:
                continue

            dx = p["tx"] - p["x"]
            dy = p["ty"] - p["y"]

            p["x"] += dx * p["speed"]
            p["y"] += dy * p["speed"]

            # Floating effect
            fx = math.sin(
                time_passed * 2 +
                p["phase"]
            ) * 0.5

            fy = math.cos(
                time_passed * 2 +
                p["phase"]
            ) * 0.5

            x = int(p["x"] + fx)
            y = int(p["y"] + fy)

            # --------------------------------
            # DRAW PARTICLE
            # --------------------------------

            pygame.draw.circle(
                screen,
                p["color"],
                (x, y),
                p["size"]
            )

        # ----------------------------------
        # SPARKLES
        # ----------------------------------

        if time_passed > 5:

            for s in sparkles:

                alpha = int(
                    150 +
                    100 * math.sin(
                        time_passed * 3 +
                        s["phase"]
                    )
                )

                alpha = max(
                    0,
                    min(255, alpha)
                )

                sparkle = pygame.Surface(
                    (6, 6),
                    pygame.SRCALPHA
                )

                pygame.draw.circle(
                    sparkle,
                    (
                        255,
                        255,
                        255,
                        alpha
                    ),
                    (3, 3),
                    s["size"]
                )

                screen.blit(
                    sparkle,
                    (
                        s["x"],
                        s["y"]
                    )
                )

        # ----------------------------------
        # FINAL IMAGE
        # ----------------------------------

        if time_passed > 55:

            fade_time = time_passed - 55

            alpha = int(
                min(
                    255,
                    fade_time * 255 / 5
                )
            )

            final_image = image.copy()

            final_image.set_alpha(
                alpha
            )

            screen.blit(
                final_image,
                (
                    image_x,
                    image_y
                )
            )

        # ----------------------------------
        # DISPLAY
        # ----------------------------------

        pygame.display.flip()

        # IMPORTANT FOR PYGBAG
        await asyncio.sleep(0)

    pygame.quit()


# ==========================================
# START
# ==========================================

asyncio.run(main())