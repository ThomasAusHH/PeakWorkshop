# Changelog

## 0.4.0 - Planets, item abilities, space skies and steadier multiplayer

Walk around planets like in Super Mario Galaxy, build items that launch you, fly, float or shoot ropes, put jump pads
and launch cannons on your maps, switch off the ocean for real space maps with your own night sky - and joining a
running round on a big map finally works smoothly.

**Heads-up for map creators**
- **Rock masses are rebuilt without holes** (see "Other fixes"). Where a wall between a tunnel and the outside is
  thinner than one grid cell, it now opens up with a clean edge. If your map has rock masses with thin walls, fly it
  once in the editor, bake the light again and publish a new revision, so other players get the same shape.
- **Maps with more than about 6,000 networked objects** (scattered items, luggage, vines, weather zones …) now work,
  but the editor, the map check and publishing warn you: they cost loading time for every player. Put items into
  luggage or scatter fewer of them.
- **Everyone in a lobby should update.** Late joining, network IDs above 6,000 and stuck limbs are fixed on each
  player's own PC.

**Planets and gravity**
- **Planets with their own gravity, like Super Mario Galaxy.** Select any object, rock mass, terrain or group in the
  editor and press "Make it a planet": a gravity field sticks to it, and players walk all the way around - upside down
  on the bottom too -, jump, fall and climb mountains on it while the camera turns with them. Choose sphere or box,
  radius, strength, a soft edge, an offset center, or "Only pull" (players stay upright and just fall onto it).
- The game follows along: items fall toward the planet, ropes and chains hang toward it, and parachutes, gliders,
  balloons, jetpacks, rivers, lava streams, pets and your own NPCs use its gravity. Oceans and lava seas can be spheres
  around a planet, and baked light and openness (storm, cold) are measured along the planet's up.
- **Scatter around a planet:** scatter areas can cover a whole planet, a cap, a ring/band or a polygon - rays come from
  outside toward the center and blocks stand upright to the surface.
- The camera turns smoothly when you jump from one planet to the next, and the editor camera can follow planet gravity
  (switch under the view cube), so placing things on the side of a planet is easy.
- New rock mass shape "Sphere" for whole planets.
- Works for every player without extra network traffic; other players no longer get stuck inside a planet on your
  screen after a fast flight.
- **New effect zone "Gravity (jumps)":** 50 % lets you jump twice as high and fall slowly, 17 % feels like the moon,
  200 % keeps you close to the ground. Jump strength follows gravity automatically (or set it up to 1000 %), and fall
  damage follows the height you actually fell.

**Item abilities**
- The item creator has a new step "Abilities" - up to four per item, combinable with any effect and the light (a
  shotgun with a recoil jump, for example):
  - **Move yourself:** cannon, rocket jump, double jump and charge-up launches; jetpack thrust; balloons tied on a
    string above your head; umbrella and glider; a parachute that opens by itself after 1.5 s of free fall; a rocket
    pack with a fuse that teammates (or you with G) light on your back.
  - **Put things into the world:** ropes, anti-ropes and rope spools, chains like the chain launcher, a grappling hook
    that pulls you to a wall or a teammate to you, cloud, shelf or bounce shroom platforms (also thrown), and pitons.
  - **A placeable cannon** like the Scout Cannon, with your own model, force and barrel angle; a yellow arc shows
    where you will land.
  - **Wear it:** hold an item like any game item, or wear it on the back like the jetpack, backpack or rocket pack, or
    on the belt like the fanny pack. Custom backpacks and fanny packs get 1-4 slots, their own weight and optionally
    visible contents.

**Jump pads and launch cannons**
- Make any solid object a jump pad (Inspector › "Make it a jump pad") or give the game's Scout Cannon your own force,
  angle and fuse. The invisible effect zone "Launch (jump pad)" throws players for updrafts, ramps and loops.
- Yellow arcs in the editor show every trajectory. Pads and zones can be unlocked by flags, and the camera stays
  steady during long tumbling flights.

**Space maps and night skies**
- Map › "Ocean & abyss" switches off the game's water and the floor at sea level - nothing but sky above and below.
  Falling below the abyss height counts like an elimination zone (lives, spectator spot; back to the last safe spot in
  a test run).
- Sky › "Stars & space": your own stars, aurora with two colors, shooting stars, milky way and nebula, each with
  strength and color, plus how lively the sky moves.

**Zones, fog and scattering**
- **Spherical effect zones** (shape bar "Sphere"): cold, fog, darkness, gravity or music as a shell around a planet;
  "Snap to planet center" puts it right on one.
- **Fog volumes from far away:** "Full strength up to" (or "Full strength at any distance") keeps a fog body dense and
  shaped kilometers away, even beyond the game camera's 1,500 m view distance. Old maps look as before.
- **Scatter areas can avoid placed objects** ("Avoid placed objects"): no more trees on platforms, roofs or temple
  tops - also around planets and in surface mode.
- **Objects without a collider** ("No collider (visual only)") for light pillars, beams, stars and veils.
- **Counter display:** Map › Game mode › "Counter display" shows a bar at the top ("Star shards ●●○○") and announces
  every increase to all players - also when a character counts in a conversation.

**Editor**
- **Align tool (L)**, like in Tinkercad: select several objects and line them up at an edge or the center on any
  axis; click one of them to keep it fixed and align the others to it.
- View menu: "Show gravity fields" and "Show teleporters".

**Workshop and lobby**
- **Players in a lobby can browse maps and suggest them to the host.** Guests now see the MAPS tab at the airport
  terminal and get "Suggest to host", which posts the map to the text chat (and pops up for the host if the workshop is
  open). Only maps that are public online can be suggested; only the host picks and starts.
- **The workshop opens much faster and pages through long lists.** The first page shows right away, the rest loads in
  the background, thumbnails only load for the tiles you see, and "My stuff" and the trash got page buttons. Creators
  with many private uploads no longer wait for each one to load.
- Browsing the workshop creates about 90 % less memory garbage, so small hitches are much rarer.

**Multiplayer fixes**
- **Players joining a running round no longer fall into the void.** On maps with several stages they were pulled back
  to the start spawn, whose stage was already hidden for them. They now join the others or the current base camp, and
  nobody is ever moved to a spot with nothing underneath.
- **Joining via lobby, code or invite builds the same world as the host again.** The build used to start before the
  player was in the room, searched every scatter area (minutes instead of seconds) and could end up different, kicked
  or disconnected. Re-joining also no longer misses the host's character or room items.
- **No more 30-160 s freeze after joining a big map.** Thousands of queued item registrations in Photon are now
  applied in one pass, and messages that piled up during the build are processed in small portions.
- **Maps with very many networked objects work again:** bells, luggage, rain zones and picked-up items failed above
  about 6,000 networked objects (in multiplayer, items could even turn into other items). Extra network ID ranges now
  cover up to about 100,000.
- **Clicking into the BepInEx console window no longer freezes the game.** Windows' QuickEdit made every log line wait
  until Esc - the game stood still and got disconnected. QuickEdit is now off for that console only (selecting text
  still works via the window menu › Edit › Mark; config `[General] ConsoleQuickEditOff`).

**Other fixes**
- **Hands, feet, head and held items no longer get stuck in custom terrain.** Ground terrain is now only solid from the
  outside for bodies and items, like the game's own rock; climbing, footsteps and scattering are unchanged.
- **Rock masses no longer show small holes** in thin tunnel walls and on rough planets (triangles were turned inside
  out); walls thinner than one grid cell open up with a clean edge.
- **Riding moving platforms is steady** - you no longer slowly slide off, also on orbiting moons.
- Teleports, spawns and revives land on the intended floor instead of on a neighboring object or inside a hollow model.
- Maps with rock masses load faster: they replay the saved scatter placement like other maps.

**Known limitations**
- Planets and item abilities are tested mostly with two players so far; please report anything odd on Discord.
- On planets, custom enemies like spiders still fall toward world down, and grass only grows on top.
- Thin platforms, floors, walls and ceilings can still hold a hand or an item now and then.

## 0.3.0 - 36 game modes, caves, real light and darkness

The biggest update so far: every map now has its own game mode (36 of them, from Battle Royale and Bomb Defusal to
Prop Hunt and Mountain Football), real baked lighting with dark caves and flashlights, rock masses for caves and
tunnels, stages that come and go like in the original game, lobby shows across several maps, and a much smoother
editor.

**Heads-up for map creators**
- **Stages now show and hide like vanilla.** Anything assigned to a stage is only active while that stage runs. If
  you only sorted something into a stage for editing, it now disappears outside of it: mark it "Also visible in
  segment N" or set it to all stages.
- **Zone fog fades across a soft edge** inside the zone (10 m by default) instead of fading in and out over time.
  Existing fog zones look a little different; "Fade" is now only smoothing.
- **The map decides which rules the host may change.** Old maps keep every rule they left open to the host.
- **Maps that use AssetBundle blocks or materials can no longer be published** - other players don't have those
  bundles and saw white surfaces. Replace them with GLB models, primitives, game materials or a look with your own
  texture.
- **Save your map once in the editor** so it gets baked lighting (see "Light and darkness").

**Game modes: one mode per map**
- Every map now has exactly one game mode with its own goal, line-up (co-op, teams or free-for-all) and rules. The
  editor has a new tab Map › Game mode with mode tiles, a "what the map still needs" checklist (one click places a
  missing zone or spawn where you look) and only the rules that matter for that mode.
- Old maps keep working: their mode is worked out from their old team settings.
- **Co-op:** Ascent (climb together; with teams, the first team at the helicopter wins; the ending can be the
  helicopter or the Nadir), Zombie survival, Scenario (your own win/lose conditions from flags and counters, with your
  own victory text), Rescue, Defense (protect an object with hit points against waves) and Escort (a cart only moves
  while players are next to it and no enemy blocks it).
- **Battle:** Last one standing, Deathmatch, Shove arena (no damage, only pushing), Gun game (every takedown gives you
  the next weapon), Skywars (islands over the void, the last player who pushed you gets the kill), Battle royale
  (shrinking zone in phases, shown as a glowing wall; you jump from a plane flying across the map, free-fall
  with WASD and open the game's parachute with Space, or drop in with the parachute directly) and Kill confirmed (collect tags).
- **Tactical rounds:** Bomb defusal (plant at site A/B, defuse with E, faster with a defuse kit, blinking and beeping
  bomb), Hostage rescue (hostages can be animated figures that sit, follow their rescuer and cheer) and Duel arena (1v1
  or 2v2, first to N rounds). Taking out the whole other team also wins a round, not only the bomb or the hostages.
- **Zones:** Domination, Summit assault (take the zones in order, each capture adds time, respawns can move up), Summit
  flag, Capture the flag and Treasure run.
- **Race:** Obstacle race and Summit race with a shared start, checkpoints, real placings, "first wins / top N qualify
  / everyone runs it out", team place points and "back to checkpoint" or "out" on falls.
- **Roles:** Hunters, Infection, Hide and seek, Tag, VIP escape and Prop hunt. Roles are rolled at departure, and the
  special role gets a short head start.
- **Prop hunt:** hiders look at a prop and press G to become it - only the kinds the map allows (crates, barrels,
  benches …), so nobody ends up as a tree. After disguising you switch to third person to see how you stand (T toggles).
  Seekers find props by shooting them; hitting a real prop costs them health. A horn gives hiders away: everyone honks
  at a fixed interval with a countdown on screen, and hiders can honk themselves with H. The keys show at the top right.
  In the editor, Map › Game mode lists every kind of prop on the map to tick, plus the horn and the miss penalty.
  Props turn with your view and stay still while you stand; X holds them in place (no moving, free look).
  Disguised players show no health bar or name tag, and found props count as losers at the end (no helicopter seat),
  even though they joined the seekers - the same goes for Infection and Hide and seek.
- **Party:** Flood (rising water or lava, standing or swimming in it puts you out), Crumbling floor, Hang on (last one
  on the wall wins), Rockfall (dodge real tumbling boulders), Hot potato (the holder runs faster, it ticks faster near
  the end, the game's dynamite goes off) and Mountain football.
- **Rules for creators:** lives (1, several or unlimited), score limit, points per takedown, penalty for falling,
  respawn delay, spawn protection (ends with your first attack), starting gear (also Workshop items, which download
  with the map), fall limit ("from spawns" sets it 25 m below the lowest spawn), time limit and who wins at time-out.
- **Mutators:** Shoves only, Downed (knocked out is not out, teammates can help you up) and Kick (the game's hidden
  kick on right mouse with empty hands, in any mode, with knockback, cooldown, damage and more adjustable).
- **Takedowns** go to the last opponent who hit or pushed you in the last 6 seconds, including falls, lava and
  elimination zones. Respawns pick the spawn furthest from living enemies.
- **HUD:** kill feed, your points and the leader under the timer, scoreboard while holding Left Alt, "BACK IN …" or
  "ELIMINATED", status lines per mode (gun game level, zone to capture, race place, role, flag or bomb carrier …), a
  zone ring and "OUTSIDE THE ZONE" for Battle royale, and new end banners such as "All waves survived!", "Mission
  complete!" or "All zones captured". Timers now sit on dark plates so they stay readable against a bright sky.
- **Spectator area:** a new zone where players who are out stand alive instead of becoming ghosts. They can walk,
  wave and talk but can't trigger anything; an "arena" zone sends them back if they jump in.
- **Rounds:** preparation (buy, no damage), fight, round end and a world reset (everyone revived and healed, dropped
  items cleared). Side swap after N rounds, round wins for the match, survivors can keep their gear, and different
  weapons each round. Late joiners come in at the next round.
- **Money and buy counters:** start money, money for takedowns, round wins and losses, planting, defusing and
  rescuing. Give any object a price on its E interaction and it becomes a buy counter ("· $500"); the item goes
  straight into your hand.
- **Mountain football:** a physics ball run by the host, kicked with the game's own kick (faster kick animation,
  costs only part of your stamina), dribbling, goals and own goals with jingle, kick-off with air horn, out of bounds
  and a scoreboard. The ball can be a basketball, coconut, snowball, stone, Bing Bong or any block. In the editor,
  "Build a pitch" lays out a whole field in one click (grass stripes, lines, flags, goals with net and spawns), and
  the test run has a practice ball.
- **Honeycomb floors** for Crumbling floor: hexagon tiles that break into shards, a builder for rings of tiles and
  whole levels below, warning colours and sounds.
- The map check reports what a mode is missing (a hill without a hold zone, defusal without a bomb site, a fall limit
  above the spawns …).

**Guns**
- Ranged items can now be real guns: full-auto, magazines with reserve ammo, reload on R (doesn't open the emote
  wheel while you hold a gun), shotgun pellets, headshot multiplier, spread while moving, muzzle climb and a scope on
  right mouse. An ammo display shows "12 / 60", a reload bar and "No ammo".
- Hit marker: every hit with a gun or thrown weapon shows a short cross at the crosshair; a found prop in Prop hunt
  flashes red with a bonk.

**King of the Hill, waves and courses**
- King of the Hill can have a moving hill (a different zone every N seconds, with a "Hill moves in …" countdown).
- Fixed: in co-op hold zones each player's game counted on its own, so one player could see a win and another not.
  The host counts now. Hold time no longer runs during the start countdown.
- Zombie waves can come from spawn zones (A, B …), chosen per enemy group. Enemy types can be taken from the Workshop
  straight into waves.
- Fixed: wave 1 started during the start countdown. If the host leaves, the waves continue with the new host.
- Obstacle courses have a shared start and the same clock on every PC, with a finish banner and ranking. Before, every
  player's game timed the course on its own and there was no winner.

**Lobby**
- **Shows:** the host can queue 2 to 12 maps, straight from the map browser. Each round uses its map's own mode.
  After each round everyone goes back to the airport, where a countdown shows the next map (5 to 60 seconds, set by
  the host); players already download it during the countdown. With "Count wins" the player list becomes the show
  leaderboard, and when the show ends the airport shows the top three with their wins.
- **Map browser:** creating a lobby or switching maps opens a browser with search and filters (game mode, line-up,
  player count, local or online, category, playable only) instead of one long list. Online maps download and get
  chosen in one click.
- The lobby page has tabs **Rules / Teams / Show**, so nothing sits far down the page any more.
- Fixed: when the host switched to a private map during a lobby, the other players got "Download failed".
- **F5: back to the airport.** When a round ends, a box offers to skip the film and stats. Solo or as host, F5 sends
  everyone back at once. Other players mark themselves ready, and once all are ready the host sends everyone after a
  short countdown. The key can be changed or turned off in the config under `[Lobby] AirportKey`.
- The lobby shows a card for the map's game mode (description, line-up, lives, mutators). Rules the map locks show as
  "Set by the map"; the rest are pickers, depending on the mode (lives, score goal, respawn, round wins, side swap,
  start money, fuse, zone timings and more).
- **"Close lobby" really closes the lobby now.** It asks first, then sends everyone to the main menu with a message.
  Before, it only locked the lobby to new players.
- Fixed: players who were kicked, banned or sent out by "Close lobby" landed on "Failed to connect to Photon
  Network". They now leave cleanly and see the reason in the main menu.
- Fixed: after switching maps in a lobby, everyone could die on spawn because the previous map's mode and fall limit
  stayed active.
- Fixed: starting a map directly from the Workshop didn't apply its game mode, so scenario and wave rounds never ended
  with a result.
- A map file that can't be read no longer sends everyone onto an empty island; the host gets a message instead.
- The key hint shows the scoreboard key during combat and race rounds.

**Light and darkness**
- **Custom maps now get real baked lighting.** The creator's game bakes it once, with PEAK's own lighting; players
  only download the file with the map. Caves and overhangs are dark, nights are really dark, and the game's lamps
  (cave lights, glow mushrooms, lava lights, torches, the respawn chest …) light up custom maps.
- It also works on graphics cards without hardware ray tracing (slower to bake). The bake runs in the background when
  you save, or from Map › Openness / Lighting. If the game crashes during a bake, the next one automatically uses smaller steps.
  New config section `[Light]` (Backend, BakeOnSave, BakeRays).
- Without a light file, brightness now follows how much sky a spot can see, so caves and overhangs are darker than
  before anyway. Storm, cold and cave plants work the same for everyone, with or without the light file.
- Fixed: on very large maps, or maps with one object far away, everything outside the original island was bright at
  night and had no storm or fog. Far-off stray objects are left out, huge maps get a coarser light grid, and the editor
  and map check list the stray objects (click one to fly there).
- Fixed: maps inside the original island's area kept the original lighting, and moved empty stages showed dark fog
  boxes.
- **Darkness:** a map-wide darkness setting (with tint) for night maps, and a new "Darkness" zone effect that darkens
  an area with remaining light, a soft edge and a tint. It looks just as dark from outside.
- **Flashlights and lanterns:** items can now give off light, as a cone or all around, switchable or always on, with
  range, colour, shadows, battery with a low-battery flicker, and a beam you can see in fog. Synced for all players.

**Caves and rock masses**
- New rock masses for real caves, tunnels, overhangs and arches, which height terrain can't make. In the editor's new
  "Cave" menu you can place a rock mass (rectangle, dome or free outline), drill a tunnel by flying through the rock,
  carve rooms, and paint on the rock with a brush (build up, carve, smooth).
- Walls, tunnel walls and overhangs are climbable; flat ceilings are not, as in the game. The terrain and grass under
  a rock mass are cut out, and caves get darker the further in you go.
- Scatter areas can place things only inside caves: on the floor, walls or ceiling (stalactites hang down).

**Stages and skies**
- Your own content now follows the game's stages: stage 2 is not visible from the start, and the previous stage
  disappears after the campfire. This also saves performance. A new "Also visible in segment N" switch keeps
  transitions like the hill with the campfire visible.
- Item spawners of later stages fill only when that stage starts, like in the game.
- Skies per stage that fade over after the campfire, and sky zones that give each player their own sky while standing
  inside (with priority for overlapping zones). New starry sky with aurora like the Nadir.

**Nadir ending**
- Maps can keep the Nadir as an ending: chosen campfires warp everyone into the Nadir, or, as in the game, you place
  the four amulets in the amulet statue. Arriving alive in the Nadir wins. The editor has a Nadir view and a movable
  amulet statue.
- Fixed: the end gate and credits hung on custom maps when the Kiln stage was switched off.
- Fixed: with your own summit, the helicopter flew in from far out of view.

**Moving, crumbling and thrown objects**
- Climbers now move along with moving and tilting walls instead of the wall sliding away under their hands.
- New motions: wobble (tilts like a spinning top) and ramp-up (motion starts calm and gets wilder).
- Shaky objects can crumble into shards instead of falling, also by the hundreds and inside moving groups, and regrow
  if wanted. Warning looks (glowing cracks, then lava) and sounds. Nothing crumbles before "GO!", spectators never
  trigger them, and late joiners see the current state.
- Rockfall: emitters can throw real rocks of several kinds and sizes, more and more often over time. The host
  calculates their flight so everyone sees the same; landed rocks are climbable, roll downhill if wanted and shatter
  later. The editor shows direction, spread and flight path.

**New shapes, looks and random variants**
- New basic shapes: hexagon column and pyramid. Basic shapes can use the game's own materials (basalt, volcanic rock
  …) and then look and sound like the island's rock.
- See-through looks: holes in patterns (nets, fences, grates) and transparent parts of PNG textures.
- Groups can appear only by chance or as one of several variants, rolled anew every round and the same for everyone.
  The editor has a preview roll.

**Zones, fog, walls and rivers**
- Effect zones can be rotated, and the rotation now counts in play (it used to be ignored). Six side handles let you
  drag one side at a time.
- New soft edge for afflictions, zone fog, push and darkness: the effect grows from 0 at the border to full strength
  after N metres.
- Large fog volumes no longer look like sharp boxes from far away: rounded corners, wavy edges and a softer edge with
  distance.
- Fog walls can be invisible in play (they still block and can't be climbed).
- Rivers and lava streams now follow the surface, also down steep walls as one smooth band, without stair steps.

**Spawning and NPCs**
- Fixed: players were sometimes flung into the air when they spawned.
- Fixed: the player who took someone out saw them keep standing. Taken-out players now fall over for 5 seconds on
  every screen.
- Fixed: feet stuck in the ground after spawning, teleporting, a lava reset or joining late, so you couldn't jump.
  Every spawn, teleport, respawn, round reset and test run now sets you down cleanly.
- NPCs and pets walk better: they step up to 0.6 m, jump up to 1.5 m and walk around walls. Pets follow your path
  through doors and around corners and appear next to you if they get stuck.
- Items given by an object interaction (a shop counter, chest or lever) now go straight into your hand.
- **Loot chests:** an interaction can roll from one of the map's shared loot pools and spill the items out, once per
  round if wanted. Interactions can also play a model's animation for everyone (a chest lid opens and stays open).
- Items handed out by actions are loaded with the map (they could be "not loaded" before), and Workshop items show
  their title instead of `item:<id>`.
- Conditions accept a bare word (`lever`) as a flag.

**Editor**
- **Simplified Chinese interface** by TFJSN (ETWML) / 由 TFJSN 汉化: pick ZH with the language button (DE → EN → ZH)
  or leave it on "auto" with the game set to Chinese. Texts newer than the translation table still show in English.
- **No more stutter:** the regular freezes, most noticeable in the Scene tab and on maps with hundreds of objects, are
  gone. In-game overlays and HUDs also create far less garbage, so there are fewer small stutters while playing.
- **Sculpting is fast:** a brush stroke on large terrain with vegetation used to rebuild everything (over 30 s); now
  it takes a fraction of a second. Vegetation in the brushed area is re-scattered once you pause for a few seconds or
  start a test run. Undoing a stroke no longer rebuilds the terrain.
- Undo no longer rebuilds the whole map after a stage was moved, and fog sphere settings apply instantly (they used
  to trigger a 30-second rebuild).
- **Scene list:** group by area group or by biome (stages in play order, transitions, "everywhere"), a "Game mode"
  block at the top (spawns, summit, mode zones, buy counters), and the list jumps to what you click in the world
  (can be turned off). Stray objects far away from the map are listed with a warning.
- **Map tab** with sub-pages Map and Game mode; the former Openness section is now "Openness / Lighting" with the
  lighting panel (state, bake button, bake on save).
- **Skies:** sky per stage, an "Overridden by" list with jumps, a starry-sky slider and a map-wide darkness section.
  Sky zones can be outlined in the world, and the status bar shows when another sky overrides the map sky.
- New effects in the zone list, now grouped: Darkness, Sky (per player) and the game-mode zones.
- Fog walls can be shown from far away as coloured outlines with their stage name. New View menu toggles for fog
  walls, sky zones and game-mode zones - off by default so the editor opens without a tangle of lines; the selected
  zone or fog wall always shows its outline. The game's music lines in the 3D view are off by default too.
- **Stretch handles:** every object except items (basic shapes, rocks, models) has side handles to stretch
  it along one axis while the opposite side stays put; the inspector has width × height × depth separately.
- **Rotation rings:** the rotate tool shows rings around the selection; drag one to turn around that axis, no
  shortcuts needed.
- Placing spawn points keeps the tool active, so you can click several in a row.
- Campfire, fog origin and fog wall labels use the map's own stage names.
- Fixed: moving a fog origin dragged its fog walls along in the editor, then they snapped back after the next rebuild.
- Fixed: picking up amulets or other display items during a test run gave the wrong item.
- Fixed: the summit marker's default position is now the real summit, not the lower Kiln respawn point.
- Fixed: editor messages covered the shape bar.
- Fixed: the Workshop opened from the Blocks palette lay behind the editor windows and couldn't be used.
- Fixed: in top or side view, scrolling in a list also zoomed the 3D view.
- Rising water and lava, motions and emitters now start when you press P and restart with every test run.

**Workshop and moderation**
- If moderation makes your content private, its page shows why. A new revision with changed content lifts the lock.
- "Featured" on the Workshop home pages can now be picked by the moderators; otherwise it stays automatic (best
  rated).
- Fixed: the Workshop no longer uses your Windows user name anywhere (it could end up as a map's author).

**Other fixes**
- Fixed missing climbing, item and footstep sounds on maps with dense forests. Looping tree sounds used up all audio
  voices; now only the nearest ones play.
- The race clock, big messages and scope view no longer stay on screen after leaving a map.
- The Workshop pass shows its full cover from behind too (other players saw a shifted cover with the page edge).
- Starting gear was skipped in the first round of a new lobby if you had played round 1 in another lobby before.
- The map check no longer reports the game's global spawners as empty on empty ("naked") maps, and it now also flags
  stray objects, maps too large for lighting, broken sky settings and variant groups with only one group.

**Known limitations**
- Many of the new modes have so far only been tested with few players; please report anything odd on Discord.
- Bomb defusal and Hostage rescue need exactly two teams.
- Prop hunt disguises and the escort cart only copy solid models (blocks made only of effects don't work).

**Licences**
- To bake light without hardware ray tracing, the mod includes unmodified compute shaders from Unity
  (Unity Companion License) and RadeonRays 4.1 (MIT, AMD). See THIRD-PARTY-NOTICES.md.

## 0.2.0 - Water, lava, text chat, fog and interactions

**Fixes**
- Fixed a crash when starting large maps for the first time (before the placement cache exists): the GPU resident
  drawer was paused while scattering and Unity freed its buffers.
- Lighting a campfire on custom maps no longer throws an error while the game quicksaves.
- Undo on a stage campfire no longer rebuilds the whole map when a stage was moved.
- The biome title at the start of a round is no longer lost behind the loading screen - it now appears once everyone
  has loaded (with the map's own segment name if it has one).
- "Play here" (P) in the editor now starts where the screen centre points, not the mouse cursor, and a hard landing
  is cushioned.
- If a fly mod (e.g. So Fly on F) throws your character "into the void" during a test run, it is reset to a safe
  spot, and the editor warns once when such a mod uses an editor key without a modifier.
- Empty ("naked") stages are really empty now: the Alpine segment and its snow piles no longer stay behind on some
  maps, and the island catalog no longer lists game objects that "naked" already removed.

**Text chat**
- Chat in Peak Workshop lobbies: Enter opens it, Enter sends, Esc closes. `/t` writes to your team only.
- Runs over the game's own Photon connection, no extra server. Lines fade out after a few seconds; can be turned off
  in the config.

**Water and lava**
- Lakes and lava pools as a box or free outline. Swim in water (jump = up, crouch = dive), with an oxygen bar while
  your head is under water and air bubbles for flooded caves. Lava warms you nearby and throws you up on contact,
  with bubbling crust and sparks.
- Rising levels: water or lava can rise over time, after a flag, or go up and down as a tide - the same for everyone.
- Rivers and lava streams: place a source and the stream finds its own way downhill, around rocks, over cliffs as a
  waterfall, ending in a pool. Uses the game's own stream materials by default. Water pushes you along and cools you
  down; lava burns.

**Burning and shaky objects**
- Any object can burn like the hot rocks of the Caldera: flames on its surface, glowing cracks, light and heat, with
  an optional condition to light or put it out.
- Any object can wobble and fall like the game's shaky rocks when someone stands on or climbs it - it tumbles down
  the slope and stays there (or comes back after a set time). The host calculates the fall so everyone sees it land
  in the same place.

**Workshop**
- Maps, assets, items and NPC packs now show how often they were downloaded.
- The NPC tab has its own start page: popular and new NPC packs, categories (bosses, shooters, hordes, creatures,
  pets, traders, attackers) and a short "build your own NPCs" guide.
- Uploading a 3D model: materials without UVs get a colour picker, textured materials can be tinted.

**Main menu**
- The Peak Workshop sign can be moved if it is in the way of another mod's menu: hold Ctrl and drag it, the chains
  follow. Ctrl + right click puts it back. The position is saved; the key can be changed (or the sign locked) in the
  config under `[Menu] SignMoveKey`.

**Fog**
- New visible fog volume for effect zones: a real fog body exactly inside the marked area (box or free outline),
  visible from outside, limited view inside. Two styles: fog bank, or sight fog that stays clear around you and only
  reveals what is far away as you get closer. Visibility, soft edges, cloudiness, colour and day/night brightness.
- The existing zone fog now fades in and out (adjustable seconds) instead of switching on and off.

**Interactions and quests**
- Any object can get an E interaction (set flags, count, give or take items, heal, teleport) - with its own name and
  text, shown with the game's own prompt. Objects that are already interactive (bell tower, luggage …) can be bound to
  a condition, and you choose whether the game's own action runs too.
- Picking up an item and entering a zone can trigger actions as well.
- Counters (e.g. ring three bells, then a gate disappears) and AND/OR conditions everywhere - in conversations,
  interactions and "only visible when".
- Locked interactions can show what is missing ("needs rope", "bells 1/3") or stay hidden as a secret.
- Messages appear in the game's own event log.
- Flags now work on maps without NPCs.

**Editor**
- Stage campfires rotate on all axes and scale like any block (mouse wheel with Ctrl/Alt/Shift); flames and light
  scale with them. The revive statue is no longer tied to the campfire - place a RespawnChest from the catalog instead.
- Campfires, fog walls and segments now show a Rotate button right next to Move.
- Scene outline: "+" adds an empty area group or layer, and entries can be dragged onto them.

## 0.1.0 - First release

Peak Workshop is here: custom maps and game modes for PEAK, made to play with friends.

**Play together**
- Lobby browser with map preview, mode and player count; private lobbies with join codes.
- Lobbies for up to 16 players, shared start countdown, teams (by hand or random) and a friendly fire switch.
- Late joiners watch as a ghost or join in - the host decides. Kick and ban, lobby settings mid-round with F6.
- Maps, assets and items download automatically when you join.

**Game modes and maps**
- King of the Hill, free-for-all PvP, team matches with time limits, zombie waves, obstacle courses, co-op climbing.
- Featured maps: Ring Arena (King of the Hill), Crashfall Valley (adventure), a free-for-all PvP map and more in the online Workshop.

**Adventures**
- NPCs with dialogue choices, trades, gifts and quests whose flags change the world (lifts, ladders, bridges).
- Boss fights with health bar, rage and helpers; pets; loot drops.

**In-game Workshop**
- Maps, 3D assets, items and NPC packs: rate, subscribe, download, update badges, 3D viewer.
- Publish public or private, report button and moderation.

**Create**
- In-game map editor: polygon scatter areas, terrain sculpting, original PEAK blocks and your own 3D models,
  moving platforms, traps and hazards, skies, music zones, spawn points, test with P.
- Item creator (food, heals, melee, ranged with projectiles and recoil, throwables, spells) and NPC builder.

**Vanilla stays untouched**
- Host Game and Play Offline are unchanged; the mod starts only from its own sign in the main menu.
- Mod lobbies use their own Photon rooms.
