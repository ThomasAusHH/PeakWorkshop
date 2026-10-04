# Changelog

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
