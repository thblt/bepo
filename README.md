# Dépôt des pilotes de la disposition BÉPO

## Introduction

Ce dépôt contient le code source permettant de générer les
« pilotes », plus exactement les descripteurs de la disposition Bépo.
Il sera utile uniquement aux personnes souhaitant *modifier* la
disposition, ou produire rapidement des descripteurs pour de nouvelles
dispositions.  Si vous souhaitez utiliser la disposition standard,
voyez plutôt le [guide d'installation sur la page du
projet](https://bepo.fr/wiki/Installation "Guides d’installation des
pilotes bépo").

*Caveat emptor*:

 1. Ce dépôt contient à la fois les sources *et* les produits finis,
    c'est-à-dire les descripteurs de disposition eux-mêmes.
 2. Ce document a été écrit pour formaliser ce que j’ai appris en
    bricolant les sources, mais ne fait pas autorité. S’il contredit
    le code, le code a raison. Si ça ne marche pas, c’est que je me
    suis trompé.

## Le compilateur et les données source

L'essentiel de la chaîne de compilation Bépo se trouve dans le
répertoire `configGenerator`, à la racine du dépôt.

### configGenerator

Le programme essentiel, `configGenerator.pl`, est écrit en Perl et
convertit une représentation abstraite en descripteurs de clavier aux
formats suivants:

 - XKB (GNU/Linux ou *BSD), pour installation globale
 - XKB (Gnu/Linux ou *BSD), pour installation locale
 - XModmap (Gnu/Linux ou *BSD)
 - XCompose (Gnu/Linux ou *BSD) (génère uniquement les touches mortes,
   à utiliser en combinaison avec un des précédents.)
 - Microsoft Keyboard Layout Creator (MSKLC) (Windows), avec touches
   virtuelles correspondant aux dispositions Azerty, Bépo, Qwertz ou
   Dvoraj.
 - Une description informelle au format HTML, destinée à la
   documentation.

Les autres formats (essentiellement OSX et des logiciels de
dactylographie) sont produits à partir de la sortie de par une série
d'outils en Python, décrits plus loin.

Pour utiliser configGenerator, appelez-le avec pour seul argument le
format que vous souhaitez générer, parmi `x_xkb_root`, `x_xkb_user`,
`x_xmodmap`, `x_compose`, `win_msklc_azerty`, `win_msklc_bepo`,
`win_msklc_qwertz`, `win_msklc_dvoraj`, par exemple:

```
./configGenerator.pl win_msklc_azerty
```

La sortie est envoyée sur la sortie standard, il faut donc rediriger
vers un fichier:

```
./configGenerator.pl x_xkb_root > bepo.xkb
```

Pour XKB, XModmap et XCompose, la sortie est utilisable directement;
pour MSKLC, une étape de compilation supplémentaire est sans doute requise avec
MSKLC, téléchargeable auprès de Microsoft.

### Les convertisseurs secondaires

Le même répertoire contient aussi une série d'outils écrits en Python
2 (et *a priori* pas compatibles 3) pour produire de nouveaux
descripteurs.  Ils lisent en général un xkb (indifféremment produit
par `x_xkb_root` ou `x_xkb_user`) et produisent de nouveaux formats.

Sauf exceptions documentées ci-dessous, ils prennent tous deux
arguments: le fichier xkb et le fichier de sortie à écrire.

#### Pour systèmes d'exploitation

 - `kbdmap.py` produit un descripteur au format kbdmap (BSD) dans
    `sortie`.
 - `keymaps.py` : produit un descripteur au format
    keymap (Linux) dans `sortie`.
 - `keytables.py` : peut-être pour le format keytables de Solaris?
 - `macosx.py` : Produit un descripteur au format macOS.
 - `wscons.py` : pour BSD?

#### Pour des outils d'apprentissage de la dactylographie

`klavaro.py`, `ktouch.py` et `typefaster.py` produisent des
   descripteurs pour les logiciels d'apprentissage de la typographie
   [Klavaro](https://klavaro.sourceforge.io/fr/index.html "Site du
   logiciel Klavaro"),
   [KTouch](https://kde.org/applications/education/org.kde.ktouch
   "Site du projet KTouch") et TypeFaster, respectivement.

#### Pour générer des schémas visuels

 - `map.py` produit des schémas ASCII de la disposition dans tous les
   états possibles.
 - `svg.py xkb préfixe` génère des schémas de la disposition décrite
   par `xkb` dans des fichiers préfixés par `préfixe`.

#### Autres

 - `symbolsConf.py` : génère `symbols.conf` à partir de `Compose`.  Ne
   prend pas d'arguments.

 - `xkb.py`, `compose.py`, `dead_keys.py`, `deadsConf.py`,
   `defaults.py`, `terminators.py` sont des librairies Python
   utilisables pour écrire d'autres convertisseurs.

### Les formats d'entrée

`configGenerator.pl` lit les fichiers suivants, dans le répertoire du
script.

 - `layout.conf`, ou la valeur de `$BEPO_LAYOUT_DESCRIPTION`, contient
   la description de la disposition.
 - `deads.conf`, ou la valeur de `$BEPO_DEADKEY_BEHAVIOUR`, contient la
   description des enchaînements sur touche morte.
 - `virtualKeys.conf`, ou la valeur de `$BEPO_VIRTUAL_KEYS`, contient
   la configuration des touches virtuelles (Windows uniquement)
 - `double-dead-keys.conf`, ou la valeur de
   `$BEPO_DOUBLE_DEADKEY_BEHAVIOUR`, décrit les touches mortes
   activées par une touche morte répétée.
 - `keys.conf`, ou la valeur de `$BEPO_KEYS_FILE`, contient les
   équivalents des noms des touches pour les différents générateurs.
 - `specialKeys.conf`, ou la valeur de `$BEPO_SPECIAL_KEYS_FILE` ???
 - `symbols.conf`, ou la valeur de `$BEPO_SYMBOLS_FILE`, fait
   correspondre les noms de caractères pour les différents
   générateurs.
 - `UnicodeData-9.0.b6.partial.fr.txt`, ou la valeur de
   `$BEPO_UNICODE_FILE`, fait correspondre les points de code UNICODE
   avec leurs noms en français.

#### layout.conf

Les lignes qui commencent par un `#` sont ignorées.

Le fichier est lu ligne à ligne. Les lignes ont le format suivant:

```
[TYPE]![TOUCHE]\t[CARACTÈRE]\t[CARACTÈRE]\t[CARACTÈRE]\t[CARACTÈRE]\t
```

 - `TYPE` est `0`, `1` ou `2`, pour une touche non-alphabétique,
   partiellement alphabétique ou alphabétique, au sens de xkb
   (détermine le comportement de capslock).  Il peut être suivi de
   `w`, qui réserve son export à Windows.

 - `CARACTÈRE` correspond, de la première à la dernière occurence, au
   caractère produit par la touche de base, puis shiftée, puis au
   niveau 3 (AltGr), puis au niveau 4 (AltGr+Shift).

 - En position 0, `0`, `1` ou `2`.

#### deads.conf

Définit le comportement des touches mortes, série de noms de caractère (pas de
touches) séparés par des espaces.  Le dernier est le caractère produit par la succession des précédents.

Le préfixe `L!` ignore la ligne pour les générateurs XKB.
