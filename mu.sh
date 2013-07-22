# mu bash completion script
#
# A hackweek gift from Marek Stopka <mstopka@opensuse.org>
# Major rewrite by Josef Reidinger <jreidinger@suse.cz>
# 2009/02/19 Allow empty spaces in repos names, Werner Fink <werner@suse.de>
#
# some TODOs:
# - complete package names for install/remove/update

_mu() {
    MU_CMDLIST=(cleanup easy extract find index mkdir view)
	MU="$(type -p mu)"

	local comp command prev cur
	local -a opts=()
	local -i ITER=0
	local IFS=$'\n'

	if test $COMP_CWORD -lt 1 ; then
		let COMP_CWORD=${#COMP_WORDS[@]}
	fi
	prev=${COMP_WORDS[COMP_CWORD-1]}
	cur=${COMP_WORDS[COMP_CWORD]}

	let ITER=COMP_CWORD
	while test $((ITER--)) -ge 0 ; do
		comp="${COMP_WORDS[ITER]}"
		if [[ "${MU_CMDLIST[@]}" =~ "${comp}" ]]; then
			command=${COMP_WORDS[ITER]}
			break;
		fi
		if [[ "${comp}" =~ "mu" ]]; then
			command="mu"
			break;
		fi
	done

    case $command in
        mu)
            opts=(${MU_CMDLIST[*]})
            COMPREPLY=($(compgen -W "${opts[*]}" -- ${cur}))
            return 0
            ;;
    esac

    IFS=$'\n'
	unset ITER comp prev cur
}

complete -F _mu -o default mu
